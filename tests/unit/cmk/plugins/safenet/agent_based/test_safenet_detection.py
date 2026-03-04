#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping

import pytest

from cmk.agent_based.internal import evaluate_snmp_detection
from cmk.plugins.safenet.agent_based.safenet_hsm import snmp_section_safenet_hsm
from cmk.plugins.safenet.agent_based.safenet_ntls import snmp_section_safenet_ntls


@pytest.mark.parametrize(
    "oid_data",
    [
        pytest.param(
            {
                ".1.3.6.1.2.1.1.2.0": ".1.3.6.1.4.1.12383.0.0.0",
            },
            id="SafeNet Luna HSM 6.x device",
        ),
        pytest.param(
            {
                ".1.3.6.1.2.1.1.2.0": ".1.3.6.1.4.1.8072.3.1.1",
            },
            id="Thales SafeNet Luna S700 Series device",
        ),
    ],
)
def test_safenet_hsm_snmp_detection(oid_data: Mapping[str, str]) -> None:
    assert evaluate_snmp_detection(
        detect_spec=snmp_section_safenet_hsm.detect, oid_value_getter=oid_data.get
    )
    assert evaluate_snmp_detection(
        detect_spec=snmp_section_safenet_ntls.detect,
        oid_value_getter=oid_data.get,
    )
