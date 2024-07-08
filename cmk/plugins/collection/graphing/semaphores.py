#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.graphing.v1 import metrics, perfometers, Title

UNIT_COUNTER = metrics.Unit(metrics.DecimalNotation(""), metrics.StrictPrecision(2))

metric_semaphores = metrics.Metric(
    name="semaphores",
    title=Title("IPC semaphores"),
    unit=UNIT_COUNTER,
    color=metrics.Color.BLUE,
)

perfometer_semaphores = perfometers.Perfometer(
    name="semaphores",
    focus_range=perfometers.FocusRange(
        perfometers.Closed(0),
        perfometers.Open(5000),
    ),
    segments=["semaphores"],
)
