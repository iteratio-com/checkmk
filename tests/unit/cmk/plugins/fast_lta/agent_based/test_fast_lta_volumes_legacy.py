#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping, Sequence

import pytest

from cmk.agent_based.v2 import Result, Service, State, StringTable
from cmk.plugins.fast_lta.agent_based.fast_lta_volumes import (
    check_fast_lta_volumes,
    discover_fast_lta_volumes,
    parse_fast_lta_volumes,
)
from cmk.plugins.lib.df import FILESYSTEM_DEFAULT_PARAMS


@pytest.fixture(name="value_store")
def fixture_value_store(monkeypatch: pytest.MonkeyPatch) -> None:
    store: dict[str, object] = {"Archiv_Test.delta": (0, 9536.7431640625)}
    monkeypatch.setattr(
        "cmk.plugins.fast_lta.agent_based.fast_lta_volumes.get_value_store",
        lambda: store,
    )


@pytest.mark.parametrize(
    "string_table, expected_discoveries",
    [
        (
            [["Archiv_Test", "1000000000000", "10000000000"], ["Archiv_Test_1", "", ""]],
            [Service(item="Archiv_Test")],
        ),
    ],
)
def test_discover_fast_lta_volumes(
    string_table: StringTable, expected_discoveries: Sequence[Service]
) -> None:
    parsed = parse_fast_lta_volumes(string_table)
    result = list(discover_fast_lta_volumes(parsed))
    assert sorted(result, key=lambda s: s.item or "") == sorted(
        expected_discoveries, key=lambda s: s.item or ""
    )


@pytest.mark.usefixtures("value_store")
@pytest.mark.parametrize(
    "item, params, string_table",
    [
        (
            "Archiv_Test",
            FILESYSTEM_DEFAULT_PARAMS,
            [["Archiv_Test", "1000000000000", "10000000000"], ["Archiv_Test_1", "", ""]],
        ),
    ],
)
def test_check_fast_lta_volumes(
    item: str, params: Mapping[str, object], string_table: StringTable
) -> None:
    parsed = parse_fast_lta_volumes(string_table)
    result = list(check_fast_lta_volumes(item, params, parsed))
    results = [r for r in result if isinstance(r, Result)]
    assert results[0].state == State.OK
    assert "Used: 1.00%" in results[0].summary
