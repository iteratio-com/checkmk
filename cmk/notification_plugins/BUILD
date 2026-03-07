load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

py_library(
    name = "cmk_notification_plugins",
    srcs = glob(["**/*.py"]),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        "//cmk/utils",
        requirement("jinja2"),
        requirement("opsgenie-sdk"),
        requirement("requests"),
        requirement("urllib3"),
    ],
)
