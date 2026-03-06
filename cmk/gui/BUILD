load("@aspect_rules_py//py:defs.bzl", "py_binary", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

exports_files([
    ".f12",
    "openapi/.f12",
    "openapi/spec/spec_generator/generate_api_spec.py",
    "wsgi/.f12",
])

py_library(
    name = "cmk_gui",
    srcs = glob(
        include = ["**/*.py"],
        exclude = [
            "**/community/**",
            "**/nonfree/**",
        ],
    ) + ["wsgi/applications/index.wsgi"],
    imports = ["../.."],
    visibility = [
        "//cmk:__subpackages__",
        "//non-free/packages/cmk-dcd:__pkg__",
        "//tests:__subpackages__",
    ],
    deps = [
        "//cmk/automations:cmk_automations",
        "//cmk/bi:cmk_bi",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/diagnostics:cmk_diagnostics",
        "//cmk/diskspace:cmk_diskspace",
        "//cmk/fields:cmk_fields",
        "//cmk/inventory:cmk_inventory",
        "//cmk/piggyback:backend",
        "//cmk/piggyback:hub",
        "//cmk/plugins:cmk_plugins",
        "//cmk/product_usage:cmk_product_usage",
        "//cmk/rrd:cmk_rrd",
        "//cmk/server_side_calls_backend:cmk_server_side_calls_backend",
        "//cmk/utils:cmk_utils",
        "//packages/cmk-ccc:archive",
        "//packages/cmk-ccc:cleanup",
        "//packages/cmk-ccc:config-path",
        "//packages/cmk-ccc:crash-reporting",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:i18n",
        "//packages/cmk-ccc:plugin-registry",
        "//packages/cmk-ccc:profile",
        "//packages/cmk-ccc:regex",
        "//packages/cmk-ccc:resulttype",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:store",
        "//packages/cmk-ccc:timeout",
        "//packages/cmk-ccc:translations",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-ccc:user",
        "//packages/cmk-ccc:version",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-crypto",
        "//packages/cmk-ec",
        "//packages/cmk-ec:event",
        "//packages/cmk-ec:syslog",
        "//packages/cmk-events",
        "//packages/cmk-livestatus-client",
        "//packages/cmk-livestatus-client:py_livestatus",
        "//packages/cmk-messaging",
        "//packages/cmk-mkp-tool",
        "//packages/cmk-plugin-apis:agent_based",
        "//packages/cmk-plugin-apis:discover_plugins",
        "//packages/cmk-plugin-apis:graphing",
        "//packages/cmk-plugin-apis:inventory_ui",
        "//packages/cmk-plugin-apis:password_store",
        "//packages/cmk-plugin-apis:rulesets",
        "//packages/cmk-plugins:aws",
        "//packages/cmk-plugins:lib",
        "//packages/cmk-shared-typing:cmk_shared_typing_py",
        "//packages/cmk-trace",
        "//packages/cmk-werks",
        requirement("apispec"),
        requirement("apispec-oneofschema"),
        requirement("cryptography"),
        requirement("docstring-parser"),
        requirement("fastapi"),
        requirement("fido2"),
        requirement("flask"),
        requirement("jinja2"),
        requirement("marshmallow"),
        requirement("marshmallow-oneofschema"),
        requirement("openapi-spec-validator"),
        requirement("icalendar"),
        requirement("opentelemetry-api"),
        requirement("opentelemetry-instrumentation-fastapi"),
        requirement("opentelemetry-instrumentation-redis"),
        requirement("opentelemetry-instrumentation-requests"),
        requirement("opentelemetry-instrumentation-wsgi"),
        requirement("opentelemetry-sdk"),
        requirement("pydantic"),
        requirement("pyprof2calltree"),
        requirement("pyparsing"),
        requirement("python-active-directory"),
        requirement("python-dateutil"),
        requirement("python-ldap"),
        requirement("pyyaml"),
        requirement("recurring_ical_events"),
        requirement("redis"),
        requirement("reportlab"),
        requirement("requests"),
        requirement("setproctitle"),
        requirement("uvicorn"),
        requirement("werkzeug"),
    ],
)

py_library(
    name = "cmk_gui_pro",
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
    ) + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/nonfree/pro/robotmk:gui",
        ],
        "@//:gpl_repo": [],
    }),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_gui",
        requirement("jinja2"),
        requirement("lxml"),
        requirement("marshmallow"),
        requirement("marshmallow-oneofschema"),
        requirement("numpy"),
        requirement("pillow"),
        requirement("pypdf"),
        requirement("pysaml2"),
        requirement("python-dateutil"),
        requirement("python-ldap"),
        requirement("redis"),
        requirement("reportlab"),
        requirement("requests"),
        requirement("roman"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/nonfree/pro/bakery",
            "//cmk/nonfree/pro/robotmk",
            "//cmk/nonfree/pro/robotmk:bakery",
            "//cmk/utils:cmk_utils_pro",
            "//non-free/packages/cmk-dcd:gui",
            "//non-free/packages/cmk-dcd:protocols",
            "//non-free/packages/cmk-mknotifyd",
        ],
        "@//:gpl_repo": [],
    }),
)

py_library(
    name = "cmk_gui_ultimate",
    srcs = glob(
        include = [
            "**/nonfree/**/ultimate/**/*.py",
        ],
        allow_empty = True,
    ) + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/nonfree/ultimate/otel:gui",
        ],
        "@//:gpl_repo": [],
    }),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_gui",
        requirement("python-dateutil"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            ":cmk_gui_pro",
            "//cmk/nonfree/ultimate/metric_backend",
            "//cmk/nonfree/ultimate/otel",
            "//cmk/utils:cmk_utils_pro",
            "//non-free/packages/cmk-otel-collector",
        ],
        "@//:gpl_repo": [],
    }),
)

py_library(
    name = "cmk_gui_cloud",
    srcs = glob(
        include = ["**/nonfree/**/cloud/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_gui",
        requirement("pyjwt"),
        requirement("redis"),
        requirement("requests"),
        requirement("urllib3"),
        requirement("werkzeug"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            ":cmk_gui_pro",
            ":cmk_gui_ultimate",
            "//cmk/utils:cmk_utils_cloud",
            "//cmk/utils:cmk_utils_pro",
        ],
        "@//:gpl_repo": [],
    }),
)

py_library(
    name = "cmk_gui_ultimatemt",
    srcs = glob(
        include = ["**/nonfree/**/ultimatemt/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_gui",
        requirement("python-dateutil"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            ":cmk_gui_pro",
            ":cmk_gui_ultimate",
            "//cmk/utils:cmk_utils_pro",
            "//cmk/utils:cmk_utils_ultimatemt",
        ],
        "@//:gpl_repo": [],
    }),
)

py_binary(
    name = "generate_api_spec",
    srcs = ["openapi/spec/spec_generator/generate_api_spec.py"],
    main = "openapi/spec/spec_generator/generate_api_spec.py",
    visibility = ["//:__subpackages__"],
    deps = select({
        "@cmk//edition:cloud": [
            "//cmk:cmk_cloud",
            "//cmk:cmk_community",
            "//cmk:cmk_pro",
            "//cmk:cmk_ultimate",
        ],
        "@cmk//edition:community": [
            "//cmk:cmk_community",
        ],
        "@cmk//edition:pro": [
            "//cmk:cmk_community",
            "//cmk:cmk_pro",
        ],
        "@cmk//edition:ultimate": [
            "//cmk:cmk_community",
            "//cmk:cmk_pro",
            "//cmk:cmk_ultimate",
        ],
        "@cmk//edition:ultimatemt": [
            "//cmk:cmk_community",
            "//cmk:cmk_pro",
            "//cmk:cmk_ultimate",
            "//cmk:cmk_ultimatemt",
        ],
    }) + [
        requirement("pyyaml"),
    ],
)

# Variant of generate_api_spec that always includes at least pro edition
# modules. Used to generate the internal OpenAPI spec for TypeScript types
# consumed by cmk-frontend-vue, which ships the same bundle for all editions.
# Limited to community + pro to avoid pulling in ultimate deps that are not
# available in all nonfree edition checkouts (e.g. pro builds strip ultimate/).
py_binary(
    name = "generate_api_spec_all_editions",
    srcs = ["openapi/spec/spec_generator/generate_api_spec.py"],
    main = "openapi/spec/spec_generator/generate_api_spec.py",
    visibility = ["//:__subpackages__"],
    deps = select({
        "@//:gpl+nonfree_repo": [
            "//cmk:cmk_community",
            "//cmk:cmk_pro",
        ],
        "@//:gpl_repo": [
            "//cmk:cmk_community",
        ],
    }) + [
        requirement("pyyaml"),
    ],
)
