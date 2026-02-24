#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# comNET GmbH, Fabian Binder - 2018-05-30

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
)
from cmk.plugins.cisco.lib_ucs import DETECT
from cmk.plugins.lib.temperature import check_temperature, TempParamType


def parse_cisco_ucs_temp_mem(string_table: StringTable) -> StringTable:
    return string_table


def discover_cisco_ucs_temp_mem(section: StringTable) -> DiscoveryResult:
    for name, _value in section:
        yield Service(item=name.split("/")[3])


def check_cisco_ucs_temp_mem(item: str, params: TempParamType, section: StringTable) -> CheckResult:
    for name, value in section:
        if name.split("/")[3] == item:
            yield from check_temperature(
                int(value),
                params,
                unique_name=f"cisco_temp_{item}",
                value_store=get_value_store(),
            )


snmp_section_cisco_ucs_temp_mem = SimpleSNMPSection(
    name="cisco_ucs_temp_mem",
    detect=DETECT,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.719.1.30.12.1",
        oids=["2", "6"],
    ),
    parse_function=parse_cisco_ucs_temp_mem,
)

check_plugin_cisco_ucs_temp_mem = CheckPlugin(
    name="cisco_ucs_temp_mem",
    service_name="Temperature Mem %s",
    discovery_function=discover_cisco_ucs_temp_mem,
    check_function=check_cisco_ucs_temp_mem,
    check_ruleset_name="temperature",
    check_default_parameters={"levels": (75.0, 85.0)},
)
