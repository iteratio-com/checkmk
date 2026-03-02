#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from __future__ import annotations

import ast
from pathlib import PurePosixPath

from cmk.astrein.framework import ASTVisitorChecker


class ABCMetaMetaclassChecker(ASTVisitorChecker):
    """Detects use of `metaclass=ABCMeta` instead of inheriting from ABC."""

    def checker_id(self) -> str:
        return "abcmeta-metaclass"

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for keyword in node.keywords:
            if keyword.arg == "metaclass" and self._is_abcmeta(keyword.value):
                self.add_error(
                    "Use `class Foo(ABC):` instead of `metaclass=ABCMeta`",
                    node,
                )
        self.generic_visit(node)

    @staticmethod
    def _is_abcmeta(node: ast.expr) -> bool:
        if isinstance(node, ast.Name) and node.id == "ABCMeta":
            return True
        if (
            isinstance(node, ast.Attribute)
            and node.attr == "ABCMeta"
            and isinstance(node.value, ast.Name)
            and node.value.id == "abc"
        ):
            return True
        return False


class HTMLDebugChecker(ASTVisitorChecker):
    """Detects calls to `html.debug(...)`."""

    def checker_id(self) -> str:
        return "html-debug"

    def visit_Call(self, node: ast.Call) -> None:
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "debug"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "html"
        ):
            self.add_error("Found html.debug call", node)
        self.generic_visit(node)


class PillowImportChecker(ASTVisitorChecker):
    """Detects direct imports of PIL. Use cmk.utils.images instead."""

    def checker_id(self) -> str:
        return "pillow-import"

    def visit_Import(self, node: ast.Import) -> None:
        if self._is_excluded():
            return
        for alias in node.names:
            if alias.name == "PIL" or alias.name.startswith("PIL."):
                self.add_error(
                    "PIL should not be used directly. Use cmk.utils.images instead.",
                    node,
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if self._is_excluded():
            return
        if node.module is not None and (node.module == "PIL" or node.module.startswith("PIL.")):
            self.add_error(
                "PIL should not be used directly. Use cmk.utils.images instead.",
                node,
            )
        self.generic_visit(node)

    def _is_excluded(self) -> bool:
        return PurePosixPath(self.file_path) == PurePosixPath(
            self.repo_root / "cmk" / "utils" / "images.py"
        )
