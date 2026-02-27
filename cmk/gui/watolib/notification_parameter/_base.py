#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Callable
from dataclasses import dataclass

from cmk.gui.valuespec import Dictionary as ValueSpecDictionary
from cmk.rulesets.internal.form_specs import DictionaryExtended
from cmk.rulesets.v1.form_specs import Dictionary


@dataclass(frozen=True, kw_only=True)
class NotificationParameter:
    ident: str
    spec: Callable[[], ValueSpecDictionary]
    form_spec: Callable[[], DictionaryExtended | Dictionary] | None = None
