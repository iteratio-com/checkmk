#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# mypy: disable-error-code="no-untyped-call"

from cmk.agent_based.internal import evaluate_snmp_detection
from cmk.agent_based.v2 import StringTable
from cmk.legacy_checks.juniper_fru import check_juniper_fru, inventory_juniper_fru
from cmk.plugins.juniper.agent_based.juniper_fru_section import snmp_section_juniper_fru

# SUP-13184
TABLE_DATA_0: StringTable = [
    ["PSM 0", "18", "2"],
    ["PSM 0 INP0", "18", "2"],
    ["PSM 0 INP1", "18", "2"],
    ["PSM 1", "18", "6"],
    ["PSM 1 INP0", "18", "6"],
    ["PSM 1 INP1", "18", "6"],
    ["PSM 2", "18", "6"],
    ["PSM 2 INP0", "18", "6"],
    ["PSM 2 INP1", "18", "6"],
    ["PSM 3", "18", "6"],
    ["PSM 3 INP0", "18", "6"],
    ["PSM 3 INP1", "18", "6"],
    ["PSM 4", "18", "6"],
    ["PSM 4 INP0", "18", "6"],
    ["PSM 4 INP1", "18", "6"],
    ["PSM 5", "18", "6"],
    ["PSM 5 INP0", "18", "6"],
    ["PSM 5 INP1", "18", "6"],
    ["PSM 6", "18", "6"],
    ["PSM 6 INP0", "18", "6"],
    ["PSM 6 INP1", "18", "6"],
    ["PSM 7", "18", "6"],
    ["PSM 7 INP0", "18", "6"],
    ["PSM 7 INP1", "18", "6"],
    ["PSM 8", "18", "2"],
    ["PSM 8 INP0", "18", "2"],
    ["PSM 8 INP1", "18", "2"],
]

# SUP-13184
TABLE_DATA_1: StringTable = [
    ["PEM 0", "7", "6"],
    ["PEM 1", "7", "6"],
    ["PEM 2", "7", "6"],
    ["PEM 3", "7", "6"],
]

# Walk data kept for detection tests
DATA_0: dict[str, str] = {
    ".1.3.6.1.2.1.1.2.0": ".1.3.6.1.4.1.2636.1.1.1.2.99",
    ".1.3.6.1.4.1.2636.3.1.15.1.5.22.1.0.0": "PSM 0",
}

DATA_1: dict[str, str] = {
    ".1.3.6.1.2.1.1.2.0": ".1.3.6.1.4.1.2636.1.1.1.2.25",
    ".1.3.6.1.4.1.2636.3.1.15.1.5.2.1.0.0": "PEM 0",
}


def test_juniper_fru() -> None:
    assert evaluate_snmp_detection(
        detect_spec=snmp_section_juniper_fru.detect, oid_value_getter=DATA_1.get
    )
    parsed = snmp_section_juniper_fru.parse_function([TABLE_DATA_1])
    assert inventory_juniper_fru(parsed, ["7"]) == [
        ("PEM 0", None),
        ("PEM 1", None),
        ("PEM 2", None),
        ("PEM 3", None),
    ]
    state, message = check_juniper_fru("PEM 1", {}, parsed)
    assert (state, message) == (0, "Operational status: online")


def test_juniper_fru_18() -> None:
    assert evaluate_snmp_detection(
        detect_spec=snmp_section_juniper_fru.detect, oid_value_getter=DATA_0.get
    )
    parsed = snmp_section_juniper_fru.parse_function([TABLE_DATA_0])
    assert inventory_juniper_fru(parsed, ["18"]) == [
        ("PSM 1", None),
        ("PSM 1 INP0", None),
        ("PSM 1 INP1", None),
        ("PSM 2", None),
        ("PSM 2 INP0", None),
        ("PSM 2 INP1", None),
        ("PSM 3", None),
        ("PSM 3 INP0", None),
        ("PSM 3 INP1", None),
        ("PSM 4", None),
        ("PSM 4 INP0", None),
        ("PSM 4 INP1", None),
        ("PSM 5", None),
        ("PSM 5 INP0", None),
        ("PSM 5 INP1", None),
        ("PSM 6", None),
        ("PSM 6 INP0", None),
        ("PSM 6 INP1", None),
        ("PSM 7", None),
        ("PSM 7 INP0", None),
        ("PSM 7 INP1", None),
    ]
    state, message = check_juniper_fru("PSM 1", {}, parsed)
    assert (state, message) == (0, "Operational status: online")
