#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)
from cmk.plugins.cisco.lib_ucs import DETECT, MAP_OPERABILITY, MAP_PRESENCE

# comNET GmbH, Fabian Binder - 2018-05-08

# .1.3.6.1.4.1.9.9.719.1.41.9.1.3  cucsProcessorUnitRn
# .1.3.6.1.4.1.9.9.719.1.41.9.1.13 cucsProcessorUnitPresence
# .1.3.6.1.4.1.9.9.719.1.41.9.1.15 cucsProcessorUnitSerial
# .1.3.6.1.4.1.9.9.719.1.41.9.1.8  cucsProcessorUnitModel
# .1.3.6.1.4.1.9.9.719.1.41.9.1.10 cucsProcessorUnitOperability


def discover_cisco_ucs_cpu(section: StringTable) -> DiscoveryResult:
    for name, presence, _serial, _model, _status in section:
        if presence != "11":  # do not discover missing units
            yield Service(item=name)


def check_cisco_ucs_cpu(item: str, section: StringTable) -> CheckResult:
    for name, presence, serial, model, status in section:
        if name == item:
            state, state_readable = MAP_OPERABILITY.get(
                status, (3, "Unknown, status code %s" % status)
            )
            presence_state, presence_readable = MAP_PRESENCE.get(
                presence, (3, "Unknown, status code %s" % presence)
            )
            yield Result(state=State(state), summary="Status: %s" % state_readable)
            yield Result(state=State(presence_state), summary="Presence: %s" % presence_readable)
            yield Result(state=State.OK, summary=f"Model: {model}, SN: {serial}")


def parse_cisco_ucs_cpu(string_table: StringTable) -> StringTable:
    return string_table


snmp_section_cisco_ucs_cpu = SimpleSNMPSection(
    name="cisco_ucs_cpu",
    detect=DETECT,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.719.1.41.9.1",
        oids=["3", "13", "15", "8", "10"],
    ),
    parse_function=parse_cisco_ucs_cpu,
)


check_plugin_cisco_ucs_cpu = CheckPlugin(
    name="cisco_ucs_cpu",
    service_name="CPU %s",
    discovery_function=discover_cisco_ucs_cpu,
    check_function=check_cisco_ucs_cpu,
)
