#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


import logging
from pathlib import Path

import pytest

import cmk.fetchers.snmp_backend._utils as utils
from cmk.fetchers.snmp_backend import StoredWalkSNMPBackend


@pytest.mark.parametrize(
    "value,expected",
    [
        ("", b""),
        ('""', b""),
        ('"B2 E0 7D 2C 4D 15 "', b"\xb2\xe0},M\x15"),
        ('"B2 E0 7D 2C 4D 15"', b"B2 E0 7D 2C 4D 15"),
    ],
)
def test_strip_snmp_value(value: str, expected: bytes) -> None:
    assert utils.strip_snmp_value(value) == expected


@pytest.mark.usefixtures("create_files")
class TestStoredWalkSNMPBackend:
    @pytest.mark.parametrize(
        "a, b, result",
        [
            ("1.2.3", "1.2.3", 0),
            ("1.2.3", ".1.2.3", 0),
            (".1.2.3", "1.2.3", 0),
            (".1.2.3", ".1.2.3", 0),
            ("1.2.3", "1.2.3.4", 0),
            ("1.2.3.4", "1.2.3", 1),
            ("1.2.3", "4.5.6", -1),
        ],
    )
    def test_compare_oids(self, a: str, b: str, result: int) -> None:
        assert StoredWalkSNMPBackend._compare_oids(a, b) == result

    def test_read_walk_data(self, tmpdir: Path) -> None:
        assert StoredWalkSNMPBackend.read_walk_from_path(
            tmpdir / "walkdata" / "1.txt", logging.getLogger("test")
        ) == [
            ".1.2.3 foo\n",
            ".1.2.4 bar\nfoobar\n",
        ]
        assert StoredWalkSNMPBackend.read_walk_from_path(
            tmpdir / "walkdata" / "2.txt", logging.getLogger("test")
        ) == [
            ".1.2.3 foo\n\n\n",
            ".1.2.5 test\n",
        ]


@pytest.fixture
def create_files(tmpdir):
    tmpdir.mkdir("walkdata")
    p1 = (tmpdir / "walkdata").join("1.txt")
    p1.write(".1.2.3 foo\n.1.2.4 bar\nfoobar\n")
    p2 = (tmpdir / "walkdata").join("2.txt")
    p2.write(".1.2.3 foo\n\n\n.1.2.5 test\n")
