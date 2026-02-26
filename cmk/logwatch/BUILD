load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "config",
    srcs = ["config.py"],
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        "//packages/cmk-plugin-apis:agent_based",
    ],
)
