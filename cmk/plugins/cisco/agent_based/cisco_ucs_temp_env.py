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


def parse_cisco_ucs_temp_env(string_table: StringTable) -> dict[str, str] | None:
    return (
        {
            "Ambient": string_table[0][0],
            "Front": string_table[0][1],
            "IO-Hub": string_table[0][2],
            "Rear": string_table[0][3],
        }
        if string_table
        else None
    )


def discover_cisco_ucs_temp_env(section: dict[str, str]) -> DiscoveryResult:
    for name in section:
        yield Service(item=name)


def check_cisco_ucs_temp_env(
    item: str, params: TempParamType, section: dict[str, str]
) -> CheckResult:
    for name, temp in section.items():
        if item == name:
            yield from check_temperature(
                int(temp),
                params,
                unique_name=f"cisco_ucs_temp_env_{name}",
                value_store=get_value_store(),
            )


snmp_section_cisco_ucs_temp_env = SimpleSNMPSection(
    name="cisco_ucs_temp_env",
    detect=DETECT,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.719.1.9.44.1",
        oids=["4", "8", "13", "21"],
    ),
    parse_function=parse_cisco_ucs_temp_env,
)

check_plugin_cisco_ucs_temp_env = CheckPlugin(
    name="cisco_ucs_temp_env",
    service_name="Temperature %s",
    discovery_function=discover_cisco_ucs_temp_env,
    check_function=check_cisco_ucs_temp_env,
    check_ruleset_name="temperature",
    check_default_parameters={"levels": (30.0, 35.0)},
)
