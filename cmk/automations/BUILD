load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

py_library(
    name = "cmk_automations",
    srcs = [
        "__init__.py",
        "automation_executor.py",
        "automation_helper.py",
        "automation_subprocess.py",
        "helper_api.py",
        "results.py",
    ],
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/utils",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:i18n",
        "//packages/cmk-ccc:plugin-registry",
        "//packages/cmk-ccc:version",
        "//packages/cmk-plugin-apis:password_store",
        "//packages/cmk-trace",
        requirement("requests"),
    ],
)
