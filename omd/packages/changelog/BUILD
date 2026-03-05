load("@aspect_rules_py//py:defs.bzl", "py_binary")
load("@bazel_skylib//rules:run_binary.bzl", "run_binary")
load("@bazel_skylib//rules:write_file.bzl", "write_file")
load("@rules_pkg//pkg:mappings.bzl", "pkg_files", "pkg_mklink")
load("@rules_pkg//pkg:tar.bzl", "pkg_tar")

write_file(
    name = "werks_utils",
    out = "werks_utils.py",
    content = [
        "import runpy",
        "runpy.run_module('cmk.werks.utils', run_name=('__main__'))",
    ],
    tags = ["manual"],
)

py_binary(
    name = "werks_utils_binary",
    srcs = [":werks_utils.py"],
    tags = ["manual"],
    deps = ["//packages/cmk-werks"],
)

run_binary(
    name = "run_werks_precompile_community",
    srcs = ["//:werks_group"],
    outs = ["werks_precompiled_community"],
    args = [
        "precompile",
        "$(location //:werks_group)",
        "--filter-by-edition",
        "community",
        "$(location werks_precompiled_community)",
    ],
    tags = ["manual"],
    tool = ":werks_utils_binary",
)

run_binary(
    name = "run_werks_precompile_pro",
    srcs = ["//:werks_group"],
    outs = ["werks_precompiled_pro"],
    args = [
        "precompile",
        "$(location //:werks_group)",
        "--filter-by-edition",
        "pro",
        "$(location werks_precompiled_pro)",
    ],
    tags = ["manual"],
    tool = ":werks_utils_binary",
)

run_binary(
    name = "run_werks_precompile_ultimate",
    srcs = ["//:werks_group"],
    outs = ["werks_precompiled_ultimate"],
    args = [
        "precompile",
        "$(location //:werks_group)",
        "--filter-by-edition",
        "ultimate",
        "$(location werks_precompiled_ultimate)",
    ],
    tags = ["manual"],
    tool = ":werks_utils_binary",
)

run_binary(
    name = "run_werks_precompile_cloud",
    srcs = ["//:werks_group"],
    outs = ["werks_precompiled_cloud"],
    args = [
        "precompile",
        "$(location //:werks_group)",
        "--filter-by-edition",
        "cloud",
        "$(location werks_precompiled_cloud)",
    ],
    tags = ["manual"],
    tool = ":werks_utils_binary",
)

run_binary(
    name = "run_werks_precompile_ultimatemt",
    srcs = ["//:werks_group"],
    outs = ["werks_precompiled_ultimatemt"],
    args = [
        "precompile",
        "$(location //:werks_group)",
        "--filter-by-edition",
        "ultimatemt",
        "$(location werks_precompiled_ultimatemt)",
    ],
    tags = ["manual"],
    tool = ":werks_utils_binary",
)

run_binary(
    name = "run_changelog",
    srcs = select({
        "@cmk//edition:cloud": [
            ":werks_precompiled_cloud",
            ":werks_precompiled_community",
            ":werks_precompiled_pro",
            ":werks_precompiled_ultimate",
        ],
        "@cmk//edition:community": [
            ":werks_precompiled_community",
        ],
        "@cmk//edition:pro": [
            ":werks_precompiled_community",
            ":werks_precompiled_pro",
        ],
        "@cmk//edition:ultimate": [
            ":werks_precompiled_community",
            ":werks_precompiled_pro",
            ":werks_precompiled_ultimate",
        ],
        "@cmk//edition:ultimatemt": [
            ":werks_precompiled_community",
            ":werks_precompiled_pro",
            ":werks_precompiled_ultimate",
            ":werks_precompiled_ultimatemt",
        ],
    }),
    outs = ["changelog_file"],
    args = [
        "changelog",
        "$(location changelog_file)",
    ] + select({
        "@cmk//edition:cloud": [
            "$(location :werks_precompiled_community)",
            "$(location :werks_precompiled_pro)",
            "$(location :werks_precompiled_ultimate)",
            "$(location :werks_precompiled_cloud)",
        ],
        "@cmk//edition:community": [
            "$(location :werks_precompiled_community)",
        ],
        "@cmk//edition:pro": [
            "$(location :werks_precompiled_community)",
            "$(location :werks_precompiled_pro)",
        ],
        "@cmk//edition:ultimate": [
            "$(location :werks_precompiled_community)",
            "$(location :werks_precompiled_pro)",
            "$(location :werks_precompiled_ultimate)",
        ],
        "@cmk//edition:ultimatemt": [
            "$(location :werks_precompiled_community)",
            "$(location :werks_precompiled_pro)",
            "$(location :werks_precompiled_ultimate)",
            "$(location :werks_precompiled_ultimatemt)",
        ],
    }),
    tags = ["manual"],
    tool = ":werks_utils_binary",
    visibility = ["@@//omd:__subpackages__"],
)

pkg_files(
    name = "changelog_pkg",
    srcs = [":changelog_file"],
    prefix = select({
        "@cmk//edition:cloud": "share/doc/check_mk_cloud",
        "@cmk//edition:community": "share/doc/check_mk_community",
        "@cmk//edition:pro": "share/doc/check_mk_pro",
        "@cmk//edition:ultimate": "share/doc/check_mk_ultimate",
        "@cmk//edition:ultimatemt": "share/doc/check_mk_ultimatemt",
    }),
    renames = {":changelog_file": "ChangeLog"},
    tags = ["manual"],
)

# One pkg_files per edition, each ships only that edition's werks under its own filename.
# The pkg_tar select below composes the right set for each edition (layering).
pkg_files(
    name = "werks_pkg_community",
    srcs = [":werks_precompiled_community"],
    prefix = "share/check_mk/werks",
    renames = {":werks_precompiled_community": "werks"},
    tags = ["manual"],
)

pkg_files(
    name = "werks_pkg_pro",
    srcs = [":werks_precompiled_pro"],
    prefix = "share/check_mk/werks",
    renames = {":werks_precompiled_pro": "werks-pro"},
    tags = ["manual"],
)

pkg_files(
    name = "werks_pkg_ultimate",
    srcs = [":werks_precompiled_ultimate"],
    prefix = "share/check_mk/werks",
    renames = {":werks_precompiled_ultimate": "werks-ultimate"},
    tags = ["manual"],
)

pkg_files(
    name = "werks_pkg_cloud",
    srcs = [":werks_precompiled_cloud"],
    prefix = "share/check_mk/werks",
    renames = {":werks_precompiled_cloud": "werks-cloud"},
    tags = ["manual"],
)

pkg_files(
    name = "werks_pkg_ultimatemt",
    srcs = [":werks_precompiled_ultimatemt"],
    prefix = "share/check_mk/werks",
    renames = {":werks_precompiled_ultimatemt": "werks-ultimatemt"},
    tags = ["manual"],
)

pkg_mklink(
    name = "changelog_link",
    link_name = "share/doc/ChangeLog",
    tags = ["manual"],
    target = "check_mk/ChangeLog",
)

pkg_tar(
    name = "changelog",
    srcs = [
        "changelog_link",
        "changelog_pkg",
    ] + select({
        "@cmk//edition:cloud": [
            "werks_pkg_cloud",
            "werks_pkg_community",
            "werks_pkg_pro",
            "werks_pkg_ultimate",
        ],
        "@cmk//edition:community": [
            "werks_pkg_community",
        ],
        "@cmk//edition:pro": [
            "werks_pkg_community",
            "werks_pkg_pro",
        ],
        "@cmk//edition:ultimate": [
            "werks_pkg_community",
            "werks_pkg_pro",
            "werks_pkg_ultimate",
        ],
        "@cmk//edition:ultimatemt": [
            "werks_pkg_community",
            "werks_pkg_pro",
            "werks_pkg_ultimate",
            "werks_pkg_ultimatemt",
        ],
    }),
    stamp = 1,
    tags = ["manual"],
    visibility = ["@@//omd:__subpackages__"],
)
