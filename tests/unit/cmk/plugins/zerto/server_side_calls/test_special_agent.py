#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping, Sequence

import pytest

from cmk.plugins.zerto.server_side_calls.special_agent import commands_function, Params
from cmk.server_side_calls.v1 import HostConfig, IPv4Config, Secret, SpecialAgentCommand


@pytest.mark.parametrize(
    ["params", "expected_args"],
    [
        pytest.param(
            {
                "username": "usr",
                "password": Secret(1),
                "cert_verification": ("secure", {"verify": True, "cert_server_name": ""}),
            },
            [
                "--authentication",
                "windows",
                "--username",
                "usr",
                "--password-id",
                Secret(1),
                "address",
                "--cert-server-name",
                "testhost",
            ],
        ),
        pytest.param(
            {
                "username": "usr",
                "password": Secret(1),
                "cert_verification": ("insecure", {"verify": False}),
            },
            [
                "--authentication",
                "windows",
                "--username",
                "usr",
                "--password-id",
                Secret(1),
                "address",
                "--disable-cert-verification",
                "--cert-server-name",
                "testhost",
            ],
        ),
        pytest.param(
            {
                "username": "usr",
                "password": Secret(1),
                "cert_verification": ("secure", {"verify": True, "cert_server_name": "temphost"}),
            },
            [
                "--authentication",
                "windows",
                "--username",
                "usr",
                "--password-id",
                Secret(1),
                "address",
                "--cert-server-name",
                "temphost",
            ],
        ),
    ],
)
def test_zerto(params: Mapping[str, object], expected_args: Sequence[str]) -> None:
    assert list(
        commands_function(
            Params.model_validate(params),
            HostConfig(name="testhost", ipv4_config=IPv4Config(address="address")),
        )
    ) == [
        SpecialAgentCommand(command_arguments=expected_args),
    ]
