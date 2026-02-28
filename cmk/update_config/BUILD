load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

py_library(
    name = "cmk_update_config",
    srcs = glob(
        include = ["**/*.py"],
        exclude = [
            "**/community/**",
            "**/nonfree/**",
        ],
    ),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        "//cmk:message_broker_certs",
        "//cmk:validate_config",
        "//cmk/base:cmk_base",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/gui:cmk_gui",
        "//cmk/utils:cmk_utils",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:plugin-registry",
        "//packages/cmk-ccc:regex",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:store",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-ccc:user",
        "//packages/cmk-ccc:version",
        "//packages/cmk-ec",
        "//packages/cmk-mkp-tool",
        "//packages/cmk-plugin-apis:agent_based",
        "//packages/cmk-plugin-apis:discover_plugins",
        "//packages/cmk-plugin-apis:graphing",
        "//packages/cmk-plugin-apis:rulesets",
        "//packages/cmk-werks",
        requirement("python-dateutil"),
    ],
)

py_library(
    name = "cmk_update_config_pro",
    srcs = glob(
        include = ["**/nonfree/**/pro/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    tags = ["no-mypy"],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_update_config",
    ],
)

py_library(
    name = "cmk_update_config_ultimate",
    srcs = glob(
        include = ["**/nonfree/**/ultimate/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    tags = ["no-mypy"],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_update_config",
    ],
)

py_library(
    name = "cmk_update_config_ultimatemt",
    srcs = glob(
        include = ["**/nonfree/**/ultimatemt/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    tags = ["no-mypy"],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_update_config",
    ],
)
