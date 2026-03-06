load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

py_library(
    name = "cmk_fields",
    srcs = [
        "__init__.py",
        "base.py",
        "primitives.py",
        "validators.py",
    ],
    imports = ["../.."],
    visibility = [
        "//cmk:__subpackages__",
        "//non-free/packages/cmk-dcd:__pkg__",
    ],
    deps = [
        "//packages/cmk-ccc:hostaddress",
        requirement("marshmallow"),
    ],
)
