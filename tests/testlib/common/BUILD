load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

py_library(
    name = "common",
    srcs = glob(["**/*.py"]),
    imports = ["../../.."],
    visibility = ["//tests:__subpackages__"],
    deps = [
        "//cmk/base:cmk_base",
        "//cmk/utils:cmk_utils",
        "//packages/cmk-trace",
        requirement("beautifulsoup4"),
        requirement("pexpect"),
        requirement("psutil"),
        requirement("pyyaml"),
    ],
)
