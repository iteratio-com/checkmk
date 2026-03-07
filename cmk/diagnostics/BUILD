load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "cmk_diagnostics",
    srcs = glob(["**/*.py"]),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        "//cmk/utils",
        "//packages/cmk-ccc:site",
    ],
)
