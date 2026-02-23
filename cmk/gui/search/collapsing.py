#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Sequence
from itertools import groupby
from typing import Protocol

from cmk.gui.i18n import _
from cmk.shared_typing.unified_search import (
    DefaultIcon,
    IconNames,
    ProviderName,
    UnifiedSearchResultCounts,
    UnifiedSearchResultItem,
    UnifiedSearchResultItemInlineButton,
)

type CollapsedResult = tuple[Sequence[UnifiedSearchResultItem], UnifiedSearchResultCounts]


class Collapser(Protocol):
    def __call__(
        self, results: Sequence[UnifiedSearchResultItem], counts: UnifiedSearchResultCounts
    ) -> CollapsedResult: ...


def get_collapser(*, provider: ProviderName | None, disabled: bool = False) -> Collapser:
    match (provider, disabled):
        case ProviderName.monitoring | None, False:
            return _collapse_items
        case _:
            return _collapse_none


def _collapse_none(
    results: Sequence[UnifiedSearchResultItem],
    counts: UnifiedSearchResultCounts,
) -> CollapsedResult:
    return results, counts


def _collapse_items(
    results: Sequence[UnifiedSearchResultItem],
    counts: UnifiedSearchResultCounts,
) -> CollapsedResult:
    collapsed_results: list[UnifiedSearchResultItem] = []
    collapsed_result_count = 0

    tr_hostsetup, tr_hostname = _("Hosts"), _("Host name")
    tr_host_keys = frozenset({tr_hostsetup, tr_hostname})

    for _title, group in groupby(results, key=lambda item: item.title):
        host_items: dict[str, UnifiedSearchResultItem] = {}
        other_items: list[UnifiedSearchResultItem] = []

        # WARN: this logic only works because of some assumptions we make about the ordering from
        # the sort algorithm. We expect the following (translated) topics:
        #   1. setup host (topic "Hosts")
        #   2. monitoring host (topic "Host name")
        # to be grouped together and in this order in the unified search result. When that changes,
        # then this functionality will no longer work.
        for item in group:
            if item.topic in tr_host_keys:
                host_items.update({item.topic: item})
            else:
                other_items.append(item)

        match host_items.get(tr_hostsetup), host_items.get(tr_hostname):
            case (UnifiedSearchResultItem() as setup, UnifiedSearchResultItem() as monitoring):
                collapsed_results.append(_collapse_host_items(monitoring, setup))
                collapsed_result_count += 1
            case (None, UnifiedSearchResultItem() as monitoring):
                collapsed_results.append(_collapse_host_items(monitoring))
            case (UnifiedSearchResultItem() as setup, None):
                collapsed_results.append(setup)
            case _:
                pass

        if other_items:
            collapsed_results.extend(other_items)

    updated_counts = UnifiedSearchResultCounts(
        total=len(collapsed_results),
        setup=counts.setup,
        monitoring=counts.monitoring,
        customize=counts.customize,
    )

    return collapsed_results, updated_counts


def _collapse_host_items(
    monitoring_item: UnifiedSearchResultItem,
    setup_item: UnifiedSearchResultItem | None = None,
) -> UnifiedSearchResultItem:
    return UnifiedSearchResultItem(
        title=monitoring_item.title,
        target=monitoring_item.target,
        provider=ProviderName.monitoring,
        topic="Hosts",
        inline_buttons=[
            UnifiedSearchResultItemInlineButton(
                target=setup_item.target,
                title=_("Edit"),
                icon=DefaultIcon(id=IconNames.edit),
            )
        ]
        if setup_item
        else None,
    )
