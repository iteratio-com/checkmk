#!/usr/bin/env python3
# Copyright (C) 2021 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping

from cmk.agent_based.v1 import check_levels as check_levels_v1
from cmk.agent_based.v2 import CheckPlugin, CheckResult, DiscoveryResult, render, Service
from cmk.plugins.lib.cpu import Section

Params = Mapping[str, str | tuple[str, tuple[float, float]]]


def discover_cpu_threads(section: Section) -> DiscoveryResult:
    if section.threads:
        yield Service()


def _get_levels(params: Params, level_name: str) -> tuple[float, float] | None:
    """
    >>> _get_levels({"levels": "no_levels"}, "levels") is None
    True

    >>> _get_levels({}, "levels") is None
    True

    >>> _get_levels({"levels": ("levels", (4, 5))}, "levels")
    (4, 5)
    """
    if level_name not in params:
        return None
    levels = params[level_name]
    if levels == "no_levels":
        return None
    assert isinstance(levels, tuple)
    return levels[1]


def check_cpu_threads(params: Params, section: Section) -> CheckResult:
    if not (threads := section.threads):
        return
    if threads.count is not None:
        yield from check_levels_v1(
            threads.count,
            metric_name="threads",
            levels_upper=_get_levels(params, "levels"),
            render_func="{:}".format,
        )
    if threads.max is not None and threads.count is not None:
        thread_usage = 100.0 * threads.count / threads.max
        yield from check_levels_v1(
            thread_usage,
            metric_name="thread_usage",
            levels_upper=_get_levels(params, "levels_percent"),
            render_func=render.percent,
            label="Usage",
        )


check_plugin_cpu_threads = CheckPlugin(
    name="cpu_threads",
    service_name="Number of threads",
    discovery_function=discover_cpu_threads,
    check_function=check_cpu_threads,
    check_default_parameters={"levels": ("levels", (2000, 4000))},
    check_ruleset_name="threads",
    sections=["cpu"],
)
