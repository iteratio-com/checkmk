#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# mypy: disable-error-code="misc"
# mypy: disable-error-code="no-untyped-def"

from collections.abc import Callable

import pytest

from cmk.agent_based.v2 import DiscoveryResult, Metric, Result, Service, State
from cmk.checkengine.plugins import (
    CheckFunction,
    CheckPluginName,
    SectionName,
    SNMPParseFunction,
)
from cmk.plugins.lib.df import FILESYSTEM_DEFAULT_PARAMS

type DiscoveryFunction = Callable[..., DiscoveryResult]

parsed = {"Archiv_Test": [("Archiv_Test", 953674.31640625, 944137.5732421875, 0)]}
check_name = "fast_lta_volumes"


@pytest.fixture(name="value_store")
def fixture_value_store(monkeypatch: pytest.MonkeyPatch) -> None:
    store: dict[str, object] = {"Archiv_Test.delta": (0, 9536.7431640625)}
    monkeypatch.setattr(
        "cmk.plugins.fast_lta.agent_based.fast_lta_volumes.get_value_store",
        lambda: store,
    )


# TODO: drop this after migration
@pytest.fixture(scope="module", name="plugin")
def _get_plugin(agent_based_plugins):
    return agent_based_plugins.check_plugins[CheckPluginName(check_name)]


# TODO: drop this after migration
@pytest.fixture(scope="module", name=f"parse_{check_name}")
def _get_parse(agent_based_plugins):
    return agent_based_plugins.snmp_sections[SectionName(check_name)].parse_function


# TODO: drop this after migration
@pytest.fixture(scope="module", name=f"discover_{check_name}")
def _get_discovery_function(plugin):
    return lambda s: plugin.discovery_function(section=s)


# TODO: drop this after migration
@pytest.fixture(scope="module", name=f"check_{check_name}")
def _get_check_function(plugin):
    return lambda i, p, s: plugin.check_function(item=i, params=p, section=s)


def test_parse_fast_lta_volumes(parse_fast_lta_volumes: SNMPParseFunction) -> None:
    assert (
        parse_fast_lta_volumes(
            [[["Archiv_Test", "1000000000000", "10000000000"], ["Archiv_Test_1", "", ""]]]
        )
        == parsed
    )


def test_discovery_fast_lta_volumes(
    discover_fast_lta_volumes: DiscoveryFunction,
) -> None:
    assert list(discover_fast_lta_volumes(parsed)) == [Service(item="Archiv_Test")]


@pytest.mark.usefixtures("value_store")
def test_check_fast_lta_volumes(
    check_fast_lta_volumes: CheckFunction,
    value_store: None,
) -> None:
    actual = list(check_fast_lta_volumes("Archiv_Test", FILESYSTEM_DEFAULT_PARAMS, parsed))
    results = [r for r in actual if isinstance(r, Result)]
    assert results[0] == Result(state=State.OK, summary="Used: 1.00% - 9.31 GiB of 931 GiB")

    metrics = [m for m in actual if isinstance(m, Metric)]
    assert metrics[0].name == "fs_used"
    assert metrics[0].value == 9536.7431640625
