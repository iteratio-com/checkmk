load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "backend",
    srcs = glob(["backend/**/*.py"]),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        "//packages/cmk-ccc:hostaddress",
    ],
)

py_library(
    name = "hub",
    srcs = glob(["hub/**/*.py"]),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":backend",
        "//packages/cmk-ccc:daemon",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-messaging",
    ],
)
