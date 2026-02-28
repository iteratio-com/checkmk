load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

exports_files([".f12"])

py_library(
    name = "cmk_base",
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
        "//cmk/automations:cmk_automations",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/core_client:cmk_core_client",
        "//cmk/diagnostics:cmk_diagnostics",
        "//cmk/inventory:cmk_inventory",
        "//cmk/piggyback:backend",
        "//cmk/rrd:cmk_rrd",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils:cmk_utils",
        "//packages/cmk-ccc:cleanup",
        "//packages/cmk-ccc:config-path",
        "//packages/cmk-ccc:cpu-tracking",
        "//packages/cmk-ccc:crash-reporting",
        "//packages/cmk-ccc:daemon",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:i18n",
        "//packages/cmk-ccc:observer",
        "//packages/cmk-ccc:plugin-registry",
        "//packages/cmk-ccc:profile",
        "//packages/cmk-ccc:regex",
        "//packages/cmk-ccc:resulttype",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:store",
        "//packages/cmk-ccc:timeout",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-ccc:user",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:helper-interface",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-crypto",
        "//packages/cmk-events",
        "//packages/cmk-livestatus-client:py_livestatus",
        "//packages/cmk-plugin-apis:agent_based",
        "//packages/cmk-plugin-apis:bakery",
        "//packages/cmk-plugin-apis:discover_plugins",
        "//packages/cmk-plugin-apis:password_store",
        "//packages/cmk-plugin-apis:server_side_calls",
        "//packages/cmk-trace",
        requirement("fastapi"),
        requirement("opentelemetry-api"),
        requirement("opentelemetry-sdk"),
        requirement("pydantic"),
        requirement("pyyaml"),
        requirement("redis"),
        requirement("setproctitle"),
        requirement("uvicorn"),
        requirement("requests"),
        requirement("watchdog"),
        requirement("opentelemetry-instrumentation-fastapi"),
    ],
)

py_library(
    name = "cmk_base_pro",
    srcs = glob(
        include = [
            "**/nonfree/**/pro/**/*.py",
            "**/nonfree/**/*.py",
        ],
        allow_empty = True,
        exclude = [
            "**/nonfree/**/cloud/**",
            "**/nonfree/**/ultimate/**",
            "**/nonfree/**/ultimatemt/**",
        ],
    ),
    imports = ["../.."],
    tags = ["no-mypy"],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_base",
    ],
)

py_library(
    name = "cmk_base_ultimate",
    srcs = glob(
        include = ["**/nonfree/**/ultimate/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    tags = ["no-mypy"],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_base",
    ],
)

py_library(
    name = "cmk_base_cloud",
    srcs = glob(
        include = ["**/nonfree/**/cloud/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    tags = ["no-mypy"],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_base",
    ],
)

py_library(
    name = "cmk_base_ultimatemt",
    srcs = glob(
        include = ["**/nonfree/**/ultimatemt/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    tags = ["no-mypy"],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_base",
    ],
)
