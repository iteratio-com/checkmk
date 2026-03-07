load("@aspect_rules_py//py:defs.bzl", "py_library")

exports_files([".f12"])

py_library(
    name = "cmk_config_anonymizer",
    srcs = glob(["**/*.py"]),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/gui",
        "//cmk/utils",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:store",
        "//packages/cmk-livestatus-client",
    ],
)
