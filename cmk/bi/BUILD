load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

py_library(
    name = "cmk_bi",
    srcs = glob(["**/*.py"]),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/fields:cmk_fields",
        "//cmk/utils:cmk_utils",
        "//packages/cmk-ccc:plugin-registry",
        "//packages/cmk-livestatus-client:py_livestatus",
        requirement("marshmallow"),
        requirement("marshmallow-oneofschema"),
        requirement("redis"),
        requirement("psutil"),
    ],
)
