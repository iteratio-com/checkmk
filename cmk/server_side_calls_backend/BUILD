load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "cmk_server_side_calls_backend",
    srcs = glob(["**/*.py"]),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        "//cmk/utils",
        "//packages/cmk-plugin-apis:discover_plugins",
        "//packages/cmk-plugin-apis:server_side_calls",
    ],
)
