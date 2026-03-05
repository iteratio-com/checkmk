#!/usr/bin/env python3
# Copyright (C) 2022 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.legacy_checks.bluecat_threads import check_bluecat_threads


def test_make_sure_bluecat_threads_can_handle_new_params_format() -> None:
    status, text, perfdata = check_bluecat_threads(  # type: ignore[no-untyped-call]
        None,
        {"levels": ("levels", (10, 20))},
        [["1234"]],
    )
    assert status == 2
    assert text == "1234 threads (critical at 20)"
    assert perfdata == [("threads", 1234, 10, 20, 0)]
