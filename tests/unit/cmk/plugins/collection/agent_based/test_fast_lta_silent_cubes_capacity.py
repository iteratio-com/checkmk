#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# mypy: disable-error-code="misc"
# mypy: disable-error-code="no-untyped-def"

from collections.abc import Callable

import pytest

from cmk.agent_based.v2 import DiscoveryResult, Metric, Result, Service, State
from cmk.checkengine.plugins import CheckFunction, CheckPluginName
from cmk.plugins.lib.df import FILESYSTEM_DEFAULT_PARAMS

type DiscoveryFunction = Callable[..., DiscoveryResult]

info = [["8001591181312", "3875508482048"]]
check_name = "fast_lta_silent_cubes_capacity"


@pytest.fixture(name="value_store")
def fixture_value_store(monkeypatch: pytest.MonkeyPatch) -> None:
    store: dict[str, object] = {"Total.delta": (0, 3695972.90234375)}
    monkeypatch.setattr(
        "cmk.legacy_checks.fast_lta_silent_cubes.get_value_store",
        lambda: store,
    )


# TODO: drop this after migration
@pytest.fixture(scope="module", name="plugin")
def _get_plugin(agent_based_plugins):
    return agent_based_plugins.check_plugins[CheckPluginName(check_name)]


# TODO: drop this after migration
@pytest.fixture(scope="module", name=f"discover_{check_name}")
def _get_discovery_function(plugin):
    return lambda s: plugin.discovery_function(section=s)


# TODO: drop this after migration
@pytest.fixture(scope="module", name=f"check_{check_name}")
def _get_check_function(plugin):
    return lambda i, p, s: plugin.check_function(item=i, params=p, section=s)


def test_discovery_fast_lta_silent_cube_capacity(
    discover_fast_lta_silent_cubes_capacity: DiscoveryFunction,
) -> None:
    assert list(discover_fast_lta_silent_cubes_capacity(info)) == [Service(item="Total")]


@pytest.mark.usefixtures("value_store")
def test_check_fast_lta_silent_cube_capacity(
    check_fast_lta_silent_cubes_capacity: CheckFunction,
    value_store: None,
) -> None:
    actual_check_results = list(
        check_fast_lta_silent_cubes_capacity("Total", FILESYSTEM_DEFAULT_PARAMS, info)
    )
    results = [r for r in actual_check_results if isinstance(r, Result)]
    assert results[0] == Result(state=State.OK, summary="Used: 48.43% - 3.52 TiB of 7.28 TiB")

    metrics = [m for m in actual_check_results if isinstance(m, Metric)]
    assert metrics[0].name == "fs_used"
    assert metrics[0].value == 3695972.90234375
