#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.agent_based.internal import evaluate_snmp_detection as evaluate
from cmk.agent_based.v2 import SNMPDetectSpecification

_INVALID_REGEX = "[invalid"


def test_evaluate_single_match() -> None:
    spec = SNMPDetectSpecification([[(".1.3.6.1.2.1.1.2.0", ".*foo.*", True)]])
    assert evaluate(detect_spec=spec, oid_value_getter={".1.3.6.1.2.1.1.2.0": "barfoo"}.get) is True


def test_evaluate_single_no_match() -> None:
    spec = SNMPDetectSpecification([[(".1.3.6.1.2.1.1.2.0", ".*foo.*", True)]])
    assert (
        evaluate(detect_spec=spec, oid_value_getter={".1.3.6.1.2.1.1.2.0": "barbaz"}.get) is False
    )


def test_evaluate_not_exists() -> None:
    spec = SNMPDetectSpecification([[(".1.3.6.1.2.1.1.2.0", ".*", False)]])
    assert evaluate(detect_spec=spec, oid_value_getter=lambda _oid: None) is True


def test_evaluate_exists() -> None:
    spec = SNMPDetectSpecification([[(".1.3.6.1.2.1.1.2.0", ".*", True)]])
    assert evaluate(detect_spec=spec, oid_value_getter=lambda _oid: None) is False


def test_evaluate_any_of() -> None:
    spec = SNMPDetectSpecification(
        [
            [(".1.3.6.1.2.1.1.2.0", ".*foo.*", True)],
            [(".1.3.6.1.2.1.1.2.0", ".*bar.*", True)],
        ]
    )
    assert (
        evaluate(detect_spec=spec, oid_value_getter={".1.3.6.1.2.1.1.2.0": "something_bar"}.get)
        is True
    )


def test_evaluate_all_of() -> None:
    spec = SNMPDetectSpecification(
        [
            [
                (".1.3.6.1.2.1.1.2.0", ".*foo.*", True),
                (".1.3.6.1.2.1.1.1.0", ".*baz.*", True),
            ],
        ]
    )
    assert (
        evaluate(
            detect_spec=spec,
            oid_value_getter={
                ".1.3.6.1.2.1.1.2.0": "afoo",
                ".1.3.6.1.2.1.1.1.0": "abaz",
            }.get,
        )
        is True
    )


def test_evaluate_all_of_partial_fail() -> None:
    spec = SNMPDetectSpecification(
        [
            [
                (".1.3.6.1.2.1.1.2.0", ".*foo.*", True),
                (".1.3.6.1.2.1.1.1.0", ".*baz.*", True),
            ],
        ]
    )
    assert (
        evaluate(
            detect_spec=spec,
            oid_value_getter={
                ".1.3.6.1.2.1.1.2.0": "afoo",
                ".1.3.6.1.2.1.1.1.0": "nope",
            }.get,
        )
        is False
    )


def test_evaluate_invalid_regex() -> None:
    spec = SNMPDetectSpecification([[(".1.3.6.1.2.1.1.2.0", _INVALID_REGEX, True)]])
    with pytest.raises(RuntimeError, match="Invalid regular expression"):
        evaluate(detect_spec=spec, oid_value_getter={".1.3.6.1.2.1.1.2.0": "value"}.get)


def test_evaluate_lazyness() -> None:
    spec = SNMPDetectSpecification(
        [
            [
                (".1.3.6.1.2.1.1.2.0", "dontmatch", True),
                (".1.3.6.1.2.1.1.3.0", _INVALID_REGEX, True),
            ],
        ]
    )
    # doesn't match, but doesn't crash either:
    assert not evaluate(detect_spec=spec, oid_value_getter={".1.3.6.1.2.1.1.2.0": "value"}.get)
