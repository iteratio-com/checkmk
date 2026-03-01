#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# mypy: disable-error-code="type-arg"

import ast
import socket
from collections.abc import Generator, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote as url_quote

from cmk.ccc.hostaddress import HostName
from cmk.ec.event import create_event_from_syslog_message
from cmk.ec.syslog import forward_to_unix_socket, SyslogMessage

_MAX_SPOOL_SIZE = 1024**2

_EC_CONNECTION_TIMEOUT = 5  # seconds


@dataclass
class ForwardedResult:
    num_forwarded: int = 0
    num_spooled: int = 0
    num_dropped: int = 0
    exception: Exception | None = None


# a) local in same omd site
# b) local pipe
# c) remote via udp
# d) remote via tcp
@dataclass(frozen=True)
class MessageForwarder:
    item: str | None
    hostname: HostName
    base_spool_path: Path
    omd_root: Path
    debug: bool

    def __call__(
        self,
        method: str | tuple,
        messages: Sequence[SyslogMessage],
        timestamp: float,
    ) -> ForwardedResult:
        if not method:
            method = str(self.omd_root / "tmp/run/mkeventd/eventsocket")
        elif isinstance(method, str) and method == "spool:":
            method += str(self.omd_root / "var/mkeventd/spool")

        if isinstance(method, tuple):
            return self._forward_tcp(
                method,
                messages,
                timestamp,
            )

        if not method.startswith("spool:"):
            return self._forward_unix_socket(
                Path(method),
                messages,
            )

        return self._forward_spool_directory(method, messages, timestamp)

    # write into local UNIX socket
    # Important: When the event daemon is stopped, then the socket
    # is *not* existing! This prevents us from hanging in such
    # situations. So we must make sure that we do not create a file
    # instead of the socket!
    @staticmethod
    def _forward_unix_socket(
        path: Path,
        events: Sequence[SyslogMessage],
    ) -> ForwardedResult:
        try:
            forward_to_unix_socket(
                events,
                path=path,
                timeout=_EC_CONNECTION_TIMEOUT,
            )
        except Exception as exc:
            return ForwardedResult(exception=exc)
        return ForwardedResult(num_forwarded=len(events))

    # Spool the log messages to given spool directory.
    # First write a file which is not read into ec, then
    # perform the move to make the file visible for ec
    def _forward_spool_directory(
        self,
        method: str,
        syslog_messages: Sequence[SyslogMessage],
        timestamp: float,
    ) -> ForwardedResult:
        if not syslog_messages:
            return ForwardedResult()

        split_files = self._split_file_messages(
            message + "\n" for message in map(repr, syslog_messages)
        )
        for file_index, file_content in enumerate(split_files):
            spool_file = self._get_new_spool_file(method, file_index, timestamp)
            with spool_file.open("w") as f:
                for message in file_content:
                    f.write(message)
            spool_file.rename(spool_file.parent / spool_file.name[1:])

        return ForwardedResult(num_forwarded=len(syslog_messages))

    @staticmethod
    def _split_file_messages(file_messages: Generator[str]) -> list[list[str]]:
        result: list[list[str]] = [[]]
        curr_file_index = 0
        curr_character_count = 0
        for file_message in file_messages:
            if curr_character_count >= _MAX_SPOOL_SIZE:
                result.append([])
                curr_file_index += 1
                curr_character_count = 0
            result[curr_file_index].append(file_message)
            curr_character_count += len(file_message)

        return result

    def _get_new_spool_file(
        self,
        method: str,
        file_index: int,
        timestamp: float,
    ) -> Path:
        spool_file = Path(
            method[6:],
            ".%s_%s%d_%d"
            % (
                self.hostname,
                (self.item.replace("/", "\\") + "_") if self.item else "",
                timestamp,
                file_index,
            ),
        )
        spool_file.parent.mkdir(parents=True, exist_ok=True)
        return spool_file

    def _forward_tcp(
        self,
        method: tuple,
        syslog_messages: Sequence[SyslogMessage],
        timestamp: float,
    ) -> ForwardedResult:
        # Transform old format: (proto, address, port)
        if not isinstance(method[1], dict):
            method = (method[0], {"address": method[1], "port": method[2]})

        result = ForwardedResult()

        message_chunks = []

        if self._shall_spool_messages(method):
            message_chunks += self._load_spooled_messages(method, result, timestamp)

        # Add chunk of new messages (when there are new ones)
        if syslog_messages:
            message_chunks.append((timestamp, 0, list(map(repr, syslog_messages))))

        if not message_chunks:
            return result  # Nothing to process

        try:
            self._forward_send_tcp(method, message_chunks, result)
        except Exception as exc:
            result.exception = exc

        # result.exception may be set in the line above, or inside _forward_send_tcp
        if result.exception:
            if self._shall_spool_messages(method):
                self._spool_messages(message_chunks, result)
            else:
                result.num_dropped = sum(len(c[2]) for c in message_chunks)

        return result

    @staticmethod
    def _shall_spool_messages(method: object) -> bool:
        return (
            isinstance(method, tuple)
            and method[0] == "tcp"
            and isinstance(method[1], dict)
            and "spool" in method[1]
        )

    @staticmethod
    def _forward_send_tcp(
        method: tuple,
        message_chunks: Iterable[tuple[float, int, list[str]]],
        result: ForwardedResult,
    ) -> None:
        protocol, method_params = method

        if protocol == "udp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif protocol == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            raise NotImplementedError()

        sock.settimeout(_EC_CONNECTION_TIMEOUT)
        sock.connect((method_params["address"], method_params["port"]))

        try:
            for _time_spooled, _num_spooled, message_chunk in message_chunks:
                for message in message_chunk:
                    sock.sendall(message.encode("utf-8") + b"\n")
                    result.num_forwarded += 1
        except Exception as exc:
            result.exception = exc
        finally:
            sock.close()

    # a) Rewrite chunks that have been processed partially
    # b) Write files for new chunk
    def _spool_messages(
        self,
        message_chunks: Iterable[tuple[float, int, list[str]]],
        result: ForwardedResult,
    ) -> None:
        self._spool_path.mkdir(parents=True, exist_ok=True)

        # Now write updated/new and delete emtpy spool files
        for time_spooled, num_already_spooled, message_chunk in message_chunks:
            spool_file_path = self._spool_path / ("spool.%0.2f" % time_spooled)

            if not message_chunk:
                # Cleanup empty spool files
                spool_file_path.unlink(missing_ok=True)
                continue

            try:
                # Partially processed chunks or the new one
                spool_file_path.write_text(repr(message_chunk))
                result.num_spooled += len(message_chunk)
            except Exception:
                if self.debug:
                    raise

                if num_already_spooled == 0:
                    result.num_dropped += len(message_chunk)

    def _update_logwatch_spoolfiles(
        self,
        old_location: Path,
    ) -> None:
        # can be removed with checkmk 2.4.0
        if self.item is None:
            # no need to update the spoolfiles if separate_checks = False
            return
        for path in old_location.glob("spool.*"):
            time_spooled = float(path.name[6:])
            messages = ast.literal_eval(path.read_text())
            if len(messages) == 0:
                continue
            event = create_event_from_syslog_message(messages[0].encode("utf-8"), None, None)
            if event["application"] == self.item:
                result = ForwardedResult()
                self._spool_messages([(time_spooled, 0, messages)], result)
                path.unlink()

    def _load_spooled_messages(
        self,
        method: tuple,
        result: ForwardedResult,
        timestamp: float,
    ) -> list[tuple[float, int, list[str]]]:
        spool_params = method[1]["spool"]

        self._update_logwatch_spoolfiles(
            old_location=self._get_spool_path(self.hostname, None),
        )

        try:
            spool_files = sorted(self._spool_path.iterdir())
        except FileNotFoundError:
            return []

        message_chunks = []

        total_size = 0
        for path in spool_files:
            # Delete unknown files
            if not path.name.startswith("spool."):
                path.unlink()
                continue

            time_spooled = float(path.name[6:])
            file_size = path.stat().st_size
            total_size += file_size

            # Delete fully processed files
            if file_size in [0, 2]:
                path.unlink()
                continue

            # TODO: this seems strange: we already added the filesize to the total_size, but now we
            # delete the file? this way total_size is too big?!

            # Delete too old files by age
            if time_spooled < timestamp - spool_params["max_age"]:
                self._spool_drop_messages(path, result)
                continue

        # Delete by size till half of target size has been deleted (oldest spool files first)
        if total_size > spool_params["max_size"]:
            target_size = int(spool_params["max_size"] / 2.0)

            for filename in spool_files:
                total_size -= self._spool_drop_messages(filename, result)
                if target_size >= total_size:
                    break  # cleaned up enough

        # Now process the remaining files
        for path in spool_files:
            time_spooled = float(path.name[6:])

            try:
                messages = ast.literal_eval(path.read_text())
                path.unlink()
            except FileNotFoundError:
                continue

            message_chunks.append((time_spooled, len(messages), messages))

        return message_chunks

    @staticmethod
    def _spool_drop_messages(path: Path, result: ForwardedResult) -> int:
        messages = ast.literal_eval(path.read_text())
        result.num_dropped += len(messages)

        file_size = path.stat().st_size
        path.unlink()
        return file_size

    @property
    def _spool_path(self) -> Path:
        return self._get_spool_path(self.hostname, self.item)

    def _get_spool_path(self, hostname: str, item: str | None) -> Path:
        result = self.base_spool_path / hostname
        return result if item is None else (result / f"item_{url_quote(item, safe='')}")
