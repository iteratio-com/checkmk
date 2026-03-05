#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


import pytest

from cmk.agent_based.v2 import Metric, Result, Service, State, StringTable
from cmk.plugins.fast_lta.agent_based.fast_lta_volumes import (
    check_fast_lta_volumes,
    discover_fast_lta_volumes,
    parse_fast_lta_volumes,
)
from cmk.plugins.lib.df import FILESYSTEM_DEFAULT_PARAMS

STRING_TABLE: StringTable = [
    ["Archiv_Test", "1000000000000", "10000000000"],
    ["Archiv_Test_1", "", ""],
]


@pytest.fixture(name="value_store")
def fixture_value_store(monkeypatch: pytest.MonkeyPatch) -> None:
    store: dict[str, object] = {"Archiv_Test.delta": (0, 9536.7431640625)}
    monkeypatch.setattr(
        "cmk.plugins.fast_lta.agent_based.fast_lta_volumes.get_value_store",
        lambda: store,
    )


def test_discovery_fast_lta_volumes() -> None:
    assert list(discover_fast_lta_volumes(parse_fast_lta_volumes(STRING_TABLE))) == [
        Service(item="Archiv_Test")
    ]


@pytest.mark.usefixtures("value_store")
def test_check_fast_lta_volumes() -> None:
    actual = list(
        check_fast_lta_volumes(
            "Archiv_Test", FILESYSTEM_DEFAULT_PARAMS, parse_fast_lta_volumes(STRING_TABLE)
        )
    )
    results = [r for r in actual if isinstance(r, Result)]
    assert results[0] == Result(state=State.OK, summary="Used: 1.00% - 9.31 GiB of 931 GiB")

    metrics = [m for m in actual if isinstance(m, Metric)]
    assert metrics[0].name == "fs_used"
    assert metrics[0].value == 9536.7431640625
