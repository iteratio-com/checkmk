#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pathlib import Path
from typing import Dict, Optional, Set

from cmk.utils.type_defs import HostAddress, HostName, SectionName, SourceType

from cmk.snmplib.type_defs import BackendSNMPTree, SNMPDetectSpec, SNMPRawData, SNMPRawDataSection

from cmk.core_helpers import FetcherType, SNMPFetcher
from cmk.core_helpers.cache import SectionStore
from cmk.core_helpers.snmp import (
    SectionMeta,
    SNMPFileCache,
    SNMPFileCacheFactory,
    SNMPHostSections,
    SNMPParser,
    SNMPPluginStore,
    SNMPPluginStoreItem,
    SNMPSummarizer,
)
from cmk.core_helpers.type_defs import Mode, NO_SELECTION, SectionNameCollection

import cmk.base.api.agent_based.register as agent_based_register
import cmk.base.check_table as check_table
import cmk.base.config as config

from ._abstract import Source


def make_inventory_sections() -> Set[SectionName]:
    return set(
        agent_based_register.get_relevant_raw_sections(
            check_plugin_names=(),
            inventory_plugin_names=(
                p.name for p in agent_based_register.iter_all_inventory_plugins()),
        )).intersection(s.name for s in agent_based_register.iter_all_snmp_sections())


def make_plugin_store() -> SNMPPluginStore:
    inventory_sections = make_inventory_sections()
    return SNMPPluginStore({
        s.name: SNMPPluginStoreItem(
            [BackendSNMPTree.from_frontend(base=t.base, oids=t.oids) for t in s.trees],
            SNMPDetectSpec(s.detect_spec),
            s.name in inventory_sections,
        ) for s in agent_based_register.iter_all_snmp_sections()
    })


class SNMPSource(Source[SNMPRawData, SNMPHostSections]):
    def __init__(
        self,
        hostname: HostName,
        ipaddress: HostAddress,
        *,
        mode: Mode,
        source_type: SourceType,
        selected_sections: SectionNameCollection,
        id_: str,
        cache_dir: Optional[Path] = None,
        persisted_section_dir: Optional[Path] = None,
        title: str,
        on_scan_error: str,
    ):
        super().__init__(
            hostname,
            ipaddress,
            mode=mode,
            source_type=source_type,
            fetcher_type=FetcherType.SNMP,
            description=SNMPSource._make_description(source_type, hostname, ipaddress, title=title),
            default_raw_data={},
            default_host_sections=SNMPHostSections(),
            id_=id_,
            cache_dir=cache_dir,
            persisted_section_dir=persisted_section_dir,
        )
        self.selected_sections = selected_sections
        if self.ipaddress is None:
            # snmp_config.ipaddress is not Optional.
            #
            # At least classic SNMP enforces that there is an address set,
            # Inline-SNMP has some lookup logic for some reason. We need
            # to find out whether or not we can really have None here.
            # Looks like it could be the case for cluster hosts which
            # don't have an IP address set.
            raise TypeError(self.ipaddress)
        self.snmp_config = (
            # Because of crap inheritance.
            self.host_config.snmp_config(self.ipaddress)
            if self.source_type is SourceType.HOST else self.host_config.management_snmp_config)
        self._on_snmp_scan_error = on_scan_error

    @classmethod
    def snmp(
        cls,
        hostname: HostName,
        ipaddress: HostAddress,
        *,
        mode: Mode,
        selected_sections: SectionNameCollection,
        on_scan_error: str,
    ) -> "SNMPSource":
        assert ipaddress is not None
        return cls(
            hostname,
            ipaddress,
            mode=mode,
            source_type=SourceType.HOST,
            selected_sections=selected_sections,
            id_="snmp",
            title="SNMP",
            on_scan_error=on_scan_error,
        )

    @classmethod
    def management_board(
        cls,
        hostname: HostName,
        ipaddress: Optional[HostAddress],
        *,
        mode: Mode,
        selected_sections: SectionNameCollection,
        on_scan_error: str,
    ) -> "SNMPSource":
        if ipaddress is None:
            raise TypeError(ipaddress)
        return cls(
            hostname,
            ipaddress,
            mode=mode,
            source_type=SourceType.MANAGEMENT,
            selected_sections=selected_sections,
            id_="mgmt_snmp",
            title="Management board - SNMP",
            on_scan_error=on_scan_error,
        )

    def _make_file_cache(self) -> SNMPFileCache:
        return SNMPFileCacheFactory(
            path=self.file_cache_path,
            simulation=config.simulation_mode,
            max_age=self.file_cache_max_age,
        ).make()

    def _make_fetcher(self) -> SNMPFetcher:
        if not SNMPFetcher.plugin_store:
            # That's a hack.
            #
            # `make_plugin_store()` depends on
            # `iter_all_snmp_sections()` and `iter_all_inventory_plugins()`
            # that are populated by the Check API upon loading the plugins.
            #
            # It is there, when the plugins are loaded, that we should
            # make the plugin store.  However, it is not clear whether
            # the API would let us register hooks to accomplish that.
            #
            # The current solution is brittle in that plugins loaded after
            # this call will be ignored or crash the fetcher.
            #
            assert config.all_checks_loaded()
            SNMPFetcher.plugin_store = make_plugin_store()
        return SNMPFetcher(
            self._make_file_cache(),
            sections=self._make_sections(),
            on_error=self._on_snmp_scan_error,
            missing_sys_description=config.get_config_cache().in_binary_hostlist(
                self.snmp_config.hostname,
                config.snmp_without_sys_descr,
            ),
            do_status_data_inventory=self.host_config.do_status_data_inventory,
            section_store_path=self.persisted_sections_file_path,
            snmp_config=self.snmp_config,
        )

    def _make_sections(self) -> Dict[SectionName, SectionMeta]:
        checking_sections = self._make_checking_sections()
        disabled_sections = self._make_disabled_sections()
        return {
            name: SectionMeta(
                checking=name in checking_sections,
                disabled=name in disabled_sections,
                fetch_interval=self.host_config.snmp_fetch_interval(name),
            ) for name in checking_sections
        }

    def _make_parser(self) -> SNMPParser:
        host_config = config.HostConfig.make_host_config(self.hostname)
        return SNMPParser(
            self.hostname,
            SectionStore[SNMPRawDataSection](
                self.persisted_sections_file_path,
                logger=self._logger,
            ),
            check_intervals={
                section_name: host_config.snmp_fetch_interval(section_name)
                for section_name in self._make_checking_sections()
            },
            keep_outdated=self.use_outdated_persisted_sections,
            logger=self._logger,
        )

    def _make_summarizer(self) -> SNMPSummarizer:
        return SNMPSummarizer(self.exit_spec)

    def _make_disabled_sections(self) -> Set[SectionName]:
        return self.host_config.disabled_snmp_sections()

    def _make_checking_sections(self) -> Set[SectionName]:
        if self.selected_sections is not NO_SELECTION:
            checking_sections = self.selected_sections
        else:
            checking_sections = set(
                agent_based_register.get_relevant_raw_sections(
                    check_plugin_names=check_table.get_needed_check_names(
                        self.hostname,
                        filter_mode="include_clustered",
                        skip_ignored=True,
                    ),
                    inventory_plugin_names=()))
        return checking_sections.intersection(
            s.name for s in agent_based_register.iter_all_snmp_sections())

    @staticmethod
    def _make_description(
        source_type: SourceType,
        hostname: HostName,
        ipaddress: HostAddress,
        *,
        title: str,
    ) -> str:
        host_config = config.get_config_cache().get_host_config(hostname)
        snmp_config = (host_config.snmp_config(ipaddress)
                       if source_type is SourceType.HOST else host_config.management_snmp_config)

        if snmp_config.is_usewalk_host:
            return "SNMP (use stored walk)"

        if snmp_config.is_snmpv3_host:
            credentials_text = "Credentials: '%s'" % ", ".join(snmp_config.credentials)
        else:
            credentials_text = "Community: %r" % snmp_config.credentials

        if snmp_config.is_snmpv3_host or snmp_config.is_bulkwalk_host:
            bulk = "yes"
        else:
            bulk = "no"

        return "%s (%s, Bulk walk: %s, Port: %d, Backend: %s)" % (
            title,
            credentials_text,
            bulk,
            snmp_config.port,
            snmp_config.snmp_backend.value,
        )
