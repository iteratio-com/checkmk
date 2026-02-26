#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from unittest.mock import patch

import pytest

from agents.plugins.mk_podman import get_piggyback_host, PiggybackNameMethod


@pytest.mark.parametrize(
    "container_id, container_name, piggyback_name_method, nodename, expected",
    [
        pytest.param(
            "",
            "mycontainer",
            PiggybackNameMethod.NAME,
            None,
            None,
            id="empty container_id returns None for NAME",
        ),
        pytest.param(
            "",
            "mycontainer",
            PiggybackNameMethod.NAME_ID,
            None,
            None,
            id="empty container_id returns None for NAME_ID",
        ),
        pytest.param(
            "",
            "mycontainer",
            PiggybackNameMethod.NODENAME_NAME,
            None,
            None,
            id="empty container_id returns None for NODENAME_NAME",
        ),
        pytest.param(
            "abc123",
            "mycontainer",
            PiggybackNameMethod.NAME,
            None,
            "mycontainer",
            id="NAME method returns container name as-is",
        ),
        pytest.param(
            "abc123def456789",
            "mycontainer",
            PiggybackNameMethod.NAME_ID,
            None,
            "mycontainer_abc123def456",
            id="NAME_ID method returns name_<first 12 chars of id>",
        ),
        pytest.param(
            "abcdefghijklmnop",
            "mycontainer",
            PiggybackNameMethod.NAME_ID,
            None,
            "mycontainer_abcdefghijkl",
            id="NAME_ID truncates id to 12 chars",
        ),
        pytest.param(
            "abc123",
            "mycontainer",
            PiggybackNameMethod.NODENAME_NAME,
            "mynode",
            "mynode_mycontainer",
            id="NODENAME_NAME with explicit nodename uses provided nodename",
        ),
        pytest.param(
            "abc123",
            "mycontainer",
            PiggybackNameMethod.NODENAME_NAME,
            None,
            "fakehost_mycontainer",
            id="NODENAME_NAME with nodename=None falls back to os.uname()[1]",
        ),
    ],
)
def test_get_piggyback_host(
    container_id: str,
    container_name: str,
    piggyback_name_method: PiggybackNameMethod,
    nodename: str | None,
    expected: str | None,
) -> None:
    with patch("os.uname", return_value=("", "fakehost", "", "", "")):
        result = get_piggyback_host(container_id, container_name, piggyback_name_method, nodename)
    assert result == expected
