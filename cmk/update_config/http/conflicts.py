#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import argparse
import enum
import re
from collections.abc import Mapping, Sequence
from contextlib import suppress
from dataclasses import dataclass
from ipaddress import AddressValueError, IPv6Address, NetmaskValueError
from typing import Literal, LiteralString

from pydantic import BaseModel, HttpUrl, ValidationError

from cmk.update_config.http.v1_scheme import V1Cert, V1Host, V1Proxy, V1Url, V1Value


class ConflictType(enum.Enum):
    http_1_0_not_supported = "http-1-0-not-supported"


class HTTP10NotSupported(enum.Enum):
    skip = "skip"
    ignore = "ignore"


@dataclass(frozen=True, kw_only=True)
class Config:
    http_1_0_not_supported: HTTP10NotSupported = HTTP10NotSupported.skip


class MigratableUrl(V1Url):
    ssl: Literal["auto", "ssl_1_2"] | None = None

    def migrate_expect_response(self) -> None | list[int]:
        if self.expect_response is None:
            return None
        return _migrate_expect_response(self.expect_response)


def _migrate_expect_response(response: list[str]) -> list[int]:
    result = []
    for item in response:
        if (status := re.search(r"\d{3}", item)) is not None:
            result.append(int(status.group()))
        else:
            raise ValueError(f"Invalid status code: {item}")
    return result


class MigratableCert(V1Cert):
    pass


class MigrateableHost(V1Host):
    address: tuple[Literal["direct"], str]


def _build_url(scheme: str, host: str, port: int | None, path: str) -> str:
    port_suffix = f":{port}" if port is not None else ""
    return f"{scheme}://{host}{port_suffix}{path}"


class MigratableValue(V1Value):
    host: MigrateableHost
    mode: tuple[Literal["url"], MigratableUrl] | tuple[Literal["cert"], MigratableCert]

    def url(self) -> str:
        scheme = "https" if self.uses_https() else "http"
        path = self.mode[1].uri or "" if isinstance(self.mode[1], MigratableUrl) else ""
        hostname = self.host.virthost or self.host.address[1]
        # TODO: currently not possible, due to proxy tunneling unavailable in V2.
        # if isinstance(address, V1Proxy):
        #     proxy = _build_url(scheme, address.address, address.port or value.host.port, path)
        #     connection["proxy"] = proxy
        return _build_url(scheme, hostname, self.host.port, path)


@dataclass(frozen=True)
class ForMigration:
    value: MigratableValue
    config: Config


@dataclass(frozen=True)
class Conflict:
    type_: LiteralString | ConflictType
    mode_fields: Sequence[str] = ()
    host_fields: Sequence[str] = ()
    disable_sni: bool = False
    cant_load: bool = False


class HostType(enum.Enum):
    IPV6 = enum.auto()
    EMBEDDABLE = enum.auto()
    INVALID = enum.auto()


def _classify(host: str) -> HostType:
    with suppress(ValidationError):
        HttpUrl(url=f"http://{host}")
        return HostType.EMBEDDABLE
    with suppress(AddressValueError, NetmaskValueError):
        IPv6Address(host)
        return HostType.IPV6
    return HostType.INVALID


def detect_conflicts(config: Config, rule_value: Mapping[str, object]) -> Conflict | ForMigration:
    try:
        value = V1Value.model_validate(rule_value)
    except ValidationError:
        return Conflict(
            type_="invalid_value",
            cant_load=True,
        )
    if value.host.address is None:
        return Conflict(
            type_="cant_migrate_address_with_macro",
            host_fields=["address"],
        )
    else:
        address = value.host.address[1]
        if isinstance(address, V1Proxy):
            return Conflict(
                type_="proxy_tunnel_not_available",
                host_fields=["address"],
            )
        elif isinstance(address, str):
            if (
                config.http_1_0_not_supported is HTTP10NotSupported.skip
                and not value.uses_https()
                and value.host.virthost is None
            ):
                return Conflict(
                    type_=ConflictType.http_1_0_not_supported,
                    host_fields=["virthost"],
                )
            type_ = _classify(address)
            if type_ is not HostType.EMBEDDABLE:
                # This might have some issues, since customers can put a port, uri, and really mess with
                # us in a multitude of ways.
                return Conflict(
                    type_="cant_turn_address_into_url",
                    host_fields=["address"],
                )
    mode = value.mode[1]
    if isinstance(mode, V1Url):
        if any(":" not in header for header in mode.add_headers or []):
            return Conflict(
                type_="add_headers_incompatible",
                mode_fields=["add_headers"],
            )
        if mode.ssl in ["ssl_1", "ssl_2", "ssl_3", "ssl_1_1"]:
            return Conflict(
                type_="ssl_incompatible",
                mode_fields=["ssl"],
            )
        if mode.expect_response_header is not None:
            if "\r\n" in mode.expect_response_header.strip("\r\n"):
                return Conflict(
                    type_="cant_match_multiple_response_header",
                    mode_fields=["expect_response_header"],
                )
            if ":" not in mode.expect_response_header:
                return Conflict(
                    type_="must_decide_whether_name_or_value",
                    mode_fields=["expect_response_header"],
                )
        if mode.expect_regex is not None and mode.expect_string is not None:
            return Conflict(
                type_="cant_have_regex_and_string",
                mode_fields=["expect_regex", "expect_string"],
            )
        if mode.method in ["OPTIONS", "TRACE", "CONNECT", "CONNECT_POST", "PROPFIND"]:
            return Conflict(
                type_="method_unavailable",
                mode_fields=["method"],
            )
        if mode.post_data is not None and mode.method in ("GET", "DELETE", "HEAD"):
            return Conflict(
                type_="cant_post_data_with_get_delete_head",
                mode_fields=["method", "post_data"],
            )
        try:
            migrated_expect_response = _migrate_expect_response(mode.expect_response or [])
        except ValueError:
            return Conflict(
                type_="only_status_codes_allowed",
                mode_fields=["expect_response"],
            )
        if value.uses_https() and value.disable_sni:
            return Conflict(
                type_="cant_disable_sni_with_https",
                mode_fields=["ssl"],
                disable_sni=True,
            )
        if migrated_expect_response and mode.onredirect in ["follow", "sticky", "stickyport"]:
            return Conflict(
                type_="v1_checks_redirect_response",
                mode_fields=["onredirect", "expect_response"],
            )
    elif value.disable_sni:  # Cert mode is always https
        return Conflict(
            type_="cant_disable_sni_with_https",
            disable_sni=True,
        )
    return ForMigration(
        value=MigratableValue.model_validate(value.model_dump()),
        config=config,
    )


class Migrate(BaseModel):
    command: Literal["migrate"]
    write: bool = False
    http_1_0_not_supported: HTTP10NotSupported


def add_migrate_parsing(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--write", action="store_true", help="persist changes on disk")
    parser.add_argument(
        f"--{ConflictType.http_1_0_not_supported.value}",
        default=HTTP10NotSupported.skip.value,
        choices=[e.value for e in HTTP10NotSupported],
        help="; ".join(
            [
                "handle missing support for HTTP/1.0",
                "skip (default): do not migrate rule",
                "ignore: use HTTP/1.1 with virtual host set to the address",
            ]
        ),
    )
