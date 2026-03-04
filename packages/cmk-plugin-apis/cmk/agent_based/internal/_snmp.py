#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import functools
import re
from collections.abc import Callable

from cmk.agent_based.v2 import SNMPDetectSpecification


def evaluate_snmp_detection(
    *,
    detect_spec: SNMPDetectSpecification,
    oid_value_getter: Callable[[str], str | None],
) -> bool:
    """Evaluate a SNMP detection specification

    Return True if and only if the conditions expressed by the spec are met
    by the `oid_value_getter`.

    The backend will pass some callback to access the SNMP device, but
    this function is written in a way that allows testing.
    """
    # TODO: add an example (as a doc test) if this is ever moved to an
    # stable API. Now we'd need imports, so we don't have a doc test.

    def _impl(atom: tuple[str, str, bool]) -> bool:
        oid, pattern, flag = atom
        value = oid_value_getter(oid)
        if value is None:
            # check for "not_exists"
            return pattern == ".*" and not flag
        # ignore case!
        return bool(_regex_cache(pattern, re.IGNORECASE | re.DOTALL).fullmatch(value)) is flag

    return any(all(_impl(atom) for atom in alternative) for alternative in detect_spec)


@functools.cache
def _regex_cache(pattern: str, flags: int) -> re.Pattern[str]:
    """Dedicated regex cache

    Compiling regex is compute intensive. So we rather cache regex which change rarely.
    """
    try:
        return re.compile(pattern, flags=flags)
    except Exception as e:
        raise RuntimeError(f"Invalid regular expression '{pattern}': {e}")
