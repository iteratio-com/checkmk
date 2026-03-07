load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "cmk_checkengine",
    srcs = glob(["**/*.py"]),
    imports = ["../.."],
    visibility = [
        "//cmk:__subpackages__",
        "//tests:__subpackages__",
    ],
    deps = [
        "//cmk/inventory:cmk_inventory",
        "//cmk/piggyback:backend",
        "//cmk/utils",
        "//packages/cmk-ccc:cpu-tracking",
        "//packages/cmk-ccc:timeout",
        "//packages/cmk-ccc:translations",
        "//packages/cmk-check-engine:helper-interface",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-plugin-apis:agent_based",
        "//packages/cmk-plugin-apis:discover_plugins",
    ],
)
