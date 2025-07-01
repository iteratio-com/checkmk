#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from dataclasses import asdict

from cmk.gui.breadcrumb import Breadcrumb
from cmk.gui.htmllib.header import make_header
from cmk.gui.htmllib.html import html
from cmk.gui.pages import PageEndpoint, PageRegistry
from cmk.gui.utils.urls import doc_reference_url

from cmk.shared_typing.welcome import WelcomePage, WelcomeUrls


def register(page_registry: PageRegistry) -> None:
    page_registry.register(PageEndpoint("welcome", _welcome_page))


def _welcome_page() -> None:
    make_header(html, "Welcome", breadcrumb=Breadcrumb(), show_top_heading=False)
    html.vue_component(
        component_name="cmk-welcome",
        data=asdict(
            WelcomePage(
                urls=WelcomeUrls(
                    checkmk_ai="https://chat.checkmk.com",
                    checkmk_forum="https://forum.checkmk.com",
                    checkmk_docs=doc_reference_url(),
                )
            )
        ),
    )
