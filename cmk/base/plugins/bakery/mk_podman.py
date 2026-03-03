#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .bakery_api.v1 import FileGenerator, OS, Plugin, PluginConfig, register

PodmanSocketDetectionMethod = (
    tuple[Literal["auto"], None]
    | tuple[Literal["only_root_socket"], None]
    | tuple[Literal["only_user_sockets"], None]
    | tuple[Literal["manual"], Sequence[str]]
)

PodmanPiggybackNameMethod = Literal["name", "nodename_name", "name_id"]


class PodmanConfig(BaseModel, frozen=True):
    deploy: bool
    socket_detection: PodmanSocketDetectionMethod
    piggyback_name_method: PodmanPiggybackNameMethod = "nodename_name"


def get_mk_podman_files(
    conf: Mapping[str, object],
) -> FileGenerator:
    confm = PodmanConfig.model_validate(conf)
    if not confm.deploy:
        return

    yield Plugin(base_os=OS.LINUX, source=Path("mk_podman.py"))

    yield PluginConfig(
        base_os=OS.LINUX,
        lines=list(_get_mk_podman_config(confm)),
        target=Path("mk_podman.cfg"),
        include_header=True,
    )


def _get_mk_podman_config(conf: PodmanConfig) -> Iterable[str]:
    yield "[PODMAN]"

    method, socket_list = conf.socket_detection
    yield f"socket_detection_method: {method}"

    if method == "manual" and socket_list:
        yield f"socket_paths: {','.join(socket_list)}"

    yield f"piggyback_name_method: {conf.piggyback_name_method}"


register.bakery_plugin(
    name="mk_podman",
    files_function=get_mk_podman_files,
)
