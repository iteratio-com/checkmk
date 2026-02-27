#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.agent_based.v2 import (
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    LevelsT,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
)
from cmk.plugins.ibm.lib import DETECT_IBM_IMM


def discover_ibm_imm_voltage(section: StringTable) -> DiscoveryResult:
    for line in section:
        yield Service(item=line[0])


def check_ibm_imm_voltage(item: str, section: StringTable) -> CheckResult:
    for line in section:
        if line[0] == item:
            volt, crit, warn, crit_low, warn_low = (float(v) / 1000 for v in line[1:])

            level_upper: LevelsT[float] = ("fixed", (warn, crit))
            level_lower: LevelsT[float] = ("fixed", (warn_low, crit_low))

            yield from check_levels(
                value=volt,
                levels_upper=level_upper,
                levels_lower=level_lower,
                render_func=lambda v: f"{v:.2f}",
                label="Volt",
                metric_name="volt",
            )


def parse_ibm_imm_voltage(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_ibm_imm_voltage = SimpleSNMPSection(
    name="ibm_imm_voltage",
    detect=DETECT_IBM_IMM,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.2.3.51.3.1.2.2.1",
        oids=["2", "3", "6", "7", "9", "10"],
    ),
    parse_function=parse_ibm_imm_voltage,
)


check_plugin_ibm_imm_voltage = CheckPlugin(
    name="ibm_imm_voltage",
    service_name="Voltage %s",
    discovery_function=discover_ibm_imm_voltage,
    check_function=check_ibm_imm_voltage,
)
