load("@aspect_rules_py//py:defs.bzl", "py_library", "py_pytest_main", "py_test")
load("@bazel_skylib//rules:write_file.bzl", "write_file")
load("@cmk_requirements//:requirements.bzl", "requirement")

package(default_visibility = [":__subpackages__"])

py_library(
    name = "conftest",
    testonly = True,
    srcs = [
        "conftest.py",
        "mocks_and_helpers.py",
    ],
    deps = [
        "//cmk/base",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/utils",
        "//packages/cmk-livestatus-client:py_livestatus",
        "//packages/cmk-plugin-apis:agent_based",
        "//tests:testlib",
        requirement("fakeredis"),
        requirement("pytest_metadata"),
    ],
)

py_library(
    name = "conftest_gui",
    testonly = True,
    srcs = [
        "cmk/gui/conftest.py",
    ],
    deps = [
        "//cmk/gui",
        "//cmk/utils",
        "//tests/testlib/unit:unit_free",
        requirement("flask"),
        requirement("pytest"),
        requirement("pytest-mock"),
    ],
)

py_pytest_main(
    name = "__test__",
    deps = [
        requirement("pytest"),
        # pytest-xdist for `--numprocesses=NPROC`
        requirement("pytest-xdist"),
    ],
)

write_file(
    name = "cannot_fail",
    out = "test_cannot_fail.py",
    content = [
        "def test_cannot_fail() -> None:",
        "    assert True",
    ],
)

py_test(
    # Start the collection and load the conftests.  The complexity
    # of those warrants this target.
    name = "smoke",
    size = "small",
    srcs = [
        "__test__.py",
        "test_cannot_fail.py",
    ],
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    deps = [
        ":__test__",
        ":conftest",
        "//tests:testlib",
    ],
)

py_test(
    name = "omdlib_unit",
    srcs = ["__test__.py"] + glob(
        include = ["omdlib/*.py"],
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    deps = [
        ":__test__",
        "//omd/packages/omd:omdlib",
        requirement("pytest-mock"),
        requirement("cryptography"),
    ],
)

py_test(
    name = "base_community",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/base/**/*.py"],
        exclude = ["**/nonfree/**"],
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        "//tests/testlib/unit:unit_free",
        requirement("pytest-mock"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
        requirement("fakeredis"),
        requirement("fastapi"),
        requirement("starlette"),
        requirement("time-machine"),
        requirement("requests"),
        requirement("watchdog"),
    ],
)

py_test(
    name = "base_pro",
    srcs = ["__test__.py"] + glob(
        # There's stuff directly under nonfree that misses the `pro` segment. Work around that:
        include = ["cmk/base/**/nonfree/**/*.py"],
        allow_empty = True,
        exclude = [
            "**/nonfree/**/cloud/**",
            "**/nonfree/**/ultimate/**",
            "**/nonfree/**/ultimatemt/**",
        ],
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        "//tests/testlib/unit:unit_free",
        requirement("protobuf"),
        requirement("pyyaml"),
        requirement("pytest-mock"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//non-free/packages/cmc-protocols:py_config_proto",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "base_ultimate",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/base/**/nonfree/**/ultimate/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        requirement("time-machine"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ],
)

py_test(
    name = "fetchers_community",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/fetchers/**/*.py"],
        exclude = ["**/nonfree/**"],
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:snmplib",
        requirement("pyghmi"),
        requirement("marshmallow"),
        requirement("pytest-mock"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ],
)

py_test(
    name = "fetchers_ultimate",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/fetchers/**/nonfree/**/ultimate/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        "//packages/cmk-ccc:resulttype",
        "//packages/cmk-check-engine:fetchers",
        "//packages/cmk-check-engine:snmplib",
        "//packages/cmk-relay-protocols",
        "//tests/testlib/unit:unit_free",
        requirement("responses"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//non-free/packages/cmk-core-helpers:relay-fetcher-trigger",
            "//non-free/packages/cmk-core-helpers:relay_trigger_protocol",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "gui_community",
    # https://bazel.build/reference/be/common-definitions#test.size
    size = "large",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/gui/**/*.py"],
        exclude = ["**/nonfree/**"],
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        requirement("apispec-oneofschema"),
        requirement("beautifulsoup4"),
        requirement("fakeredis"),
        requirement("fastapi"),
        requirement("flask"),
        requirement("marshmallow"),
        requirement("marshmallow-oneofschema"),
        requirement("openapi-spec-validator"),
        requirement("opentelemetry-sdk"),
        requirement("polyfactory"),
        requirement("pytest-mock"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
        requirement("python-dateutil"),
        requirement("python-ldap"),
        requirement("pyyaml"),
        requirement("responses"),
        requirement("time-machine"),
        requirement("werkzeug"),
        "//cmk:validate_config",
        "//cmk/bi:cmk_bi",
        "//cmk/gui",
        "//omd/packages/omd:omdlib",
        "//tests/testlib/unit:unit_free",
    ],
)

py_test(
    name = "gui_pro",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/gui/**/nonfree/**/pro/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"] + glob(
        include = [
            "**/saml2/**/*.xml",
            "**/saml2/**/*.pem",
        ],
        allow_empty = True,
    ),
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        ":conftest_gui",
        "//cmk/utils",
        "//tests/testlib/unit:unit_free",
        requirement("fakeredis"),
        requirement("lxml"),
        requirement("numpy"),
        requirement("pypdf"),
        requirement("pytest-asyncio"),
        requirement("pysaml2"),
        requirement("pytest"),
        requirement("pytest-random-order"),
        requirement("pytest-mock"),
        requirement("responses"),
        requirement("time-machine"),
        requirement("werkzeug"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/gui:pro",
            "//tests/testlib/unit:unit_nonfree",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "gui_cloud",
    srcs = [
        "__test__.py",
    ] + glob(
        include = ["cmk/gui/**/nonfree/**/cloud/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        ":conftest_gui",
        "//cmk/gui",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:user",
        "//packages/cmk-ccc:version",
        requirement("pytest"),
        requirement("pytest-mock"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
        requirement("requests"),
        requirement("responses"),
        requirement("werkzeug"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/gui:cloud",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "gui_ultimate",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/gui/**/nonfree/**/ultimate/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        ":conftest_gui",
        "//cmk/gui",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:site",
        "//tests/testlib/unit:unit_free",
        requirement("python-dateutil"),
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/gui:ultimate",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "gui_ultimatemt",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/gui/**/nonfree/**/ultimatemt/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"],
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        ":conftest",
        ":conftest_gui",
        "//tests/testlib/unit:unit_free",
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/gui:ultimatemt",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "plugins",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/plugins/**/*.py"],
        exclude = [
            "**/nonfree/**",
        ],
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"] + glob(
        include = [
            "**/_check_form_submit_response",
            "**/*.json",
            "**/*.yaml",
        ],
    ),
    main = ":__test__.py",
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        "//cmk/legacy_checks:cmk_legacy_checks",
        "//cmk/plugins:cmk_plugins",
        "//tests/testlib/unit:unit_free",
        requirement("exchangelib"),
        requirement("feedparser"),
        requirement("google-cloud-monitoring"),
        requirement("polyfactory"),
        requirement("pysmb"),
        requirement("pytest"),
        requirement("pytest-mock"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
        requirement("python-snap7"),
        requirement("requests"),
        requirement("responses"),
        requirement("time-machine"),
        requirement("vcrpy"),
    ],
)

py_test(
    name = "plugins_pro",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/plugins/**/nonfree/**/pro/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"] + glob(
        include = ["**/*.xml"],
        allow_empty = True,
    ),
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        requirement("polyfactory"),
        requirement("marshmallow"),
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/plugins:cmk_plugins_robotmk_nonfree_srcs",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "plugins_ultimate",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/plugins/**/nonfree/**/ultimate/**/*.py"],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"] + glob(
        include = ["**/*.jsonl"],
        allow_empty = True,
    ),
    main = ":__test__.py",
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        requirement("google-cloud-monitoring"),
        requirement("polyfactory"),
        requirement("opentelemetry-exporter-otlp"),
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
        requirement("time-machine"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/plugins:cmk_plugins_otel_nonfree_srcs",
            "//cmk/plugins:cmk_plugins_ultimate",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "repo",
    # https://bazel.build/reference/be/common-definitions#test.size
    size = "large",
    srcs = [
        "__init__.py",
        "__test__.py",
    ] + glob(
        # This is the "catch all" target. Don't add new stuff here.
        include = [
            "agents/**/*.py",
            "cmk/*.py",
            "cmk/automations/**/*.py",
            "cmk/bi/**/*.py",
            "cmk/checkengine/**/*.py",
            "cmk/diagnostics/**/*.py",
            "cmk/diskspace/**/*.py",
            "cmk/fields/**/*.py",
            "cmk/inventory/**/*.py",
            "cmk/legacy_checks/**/*.py",
            "cmk/legacy_includes/**/*.py",
            "cmk/nonfree/**/*.py",
            "cmk/notifications/**/*.py",
            "cmk/piggyback_hub/**/*.py",
            "cmk/piggyback/**/*.py",
            "cmk/plugins/**/*.py",
            "cmk/post_rename_site/**/*.py",
            "cmk/product_usage/**/*.py",
            "cmk/server_side_calls_backend/**/*.py",
            "cmk/snmplib/**/*.py",
            "cmk/special_agents/**/*.py",
            "cmk/update_config/**/*.py",
            "cmk/utils/**/*.py",
            "livestatus/**/*.py",
            "testlib/**/*.py",
        ],
        allow_empty = True,
    ),
    args = [
        "--config-file=$(location @//:pyproject.toml)",
        "--import-mode=importlib",
        "--random-order-bucket=global",
        "--dist=loadfile",
        "--numprocesses=4",
    ],
    data = ["@//:pyproject.toml"] + glob(
        include = [
            # canned data
            "**/_check_form_submit_response",
            "**/test-files/**",
            "**/tree_test_data/**",
            "**/*.json",
            "**/*.jsonl",
            "**/*.log",
            "**/*.yaml",
        ],
        allow_empty = True,
        exclude = ["**/*.py"],
    ) + select({
        "@//:gpl+nonfree_repo": glob(
            [
                "**/*.xml",
                "**/*.pem",
            ],
            allow_empty = True,
        ),
        "@//:gpl_repo": [],
    }),
    main = ":__test__.py",
    visibility = ["//tests:__subpackages__"],
    deps = [
        ":__test__",
        requirement("aiohttp"),
        requirement("apispec-oneofschema"),
        requirement("bcrypt"),
        requirement("beautifulsoup4"),
        requirement("coverage"),
        requirement("docstring-parser"),
        requirement("exchangelib"),
        requirement("fakeredis"),
        requirement("fastapi"),
        requirement("feedparser"),
        requirement("flask"),
        requirement("google-api-core"),
        requirement("google-api-python-client"),
        requirement("google-auth"),
        requirement("google-cloud-asset"),
        requirement("google-cloud-monitoring"),
        requirement("httpx"),
        requirement("icalendar"),
        requirement("lxml"),
        requirement("marshmallow"),
        requirement("marshmallow-oneofschema"),
        requirement("msal"),
        requirement("numpy"),
        requirement("openapi-spec-validator"),
        requirement("opentelemetry-exporter-otlp"),
        requirement("opentelemetry-instrumentation-fastapi"),
        requirement("opentelemetry-sdk"),
        requirement("pika"),
        requirement("pillow"),
        requirement("polyfactory"),
        requirement("protobuf"),
        requirement("psutil"),
        requirement("pyasn1"),
        requirement("pyghmi"),
        requirement("pyjwt"),
        requirement("pypdf"),
        requirement("pyprof2calltree"),
        requirement("pysaml2"),
        requirement("pysmb"),
        requirement("pytest-asyncio"),
        requirement("pytest-mock"),
        requirement("pytest-random-order"),
        requirement("python-active-directory"),  # missing wheel
        requirement("python-dateutil"),
        requirement("python-ldap"),
        requirement("python-snap7"),
        requirement("pyyaml"),
        requirement("recurring-ical-events"),
        requirement("redis"),
        requirement("requests"),
        requirement("responses"),
        requirement("robotframework"),
        requirement("roman"),
        requirement("setproctitle"),
        requirement("tenacity"),
        requirement("time-machine"),
        requirement("vcrpy"),
        requirement("watchdog"),
        requirement("werkzeug"),
        "//agents/plugins:apache_status",
        "//agents/plugins:nginx_status",
        "//cmk/editions:community",
        "//omd/packages/omd:omdlib",
        "//tests/testlib/unit:unit_free",
        "//tests/unit:conftest",
    ] + select({
        "@//:gpl+nonfree_repo": [
            requirement("python-multipart"),
            "//cmk/editions/nonfree:cloud",
            "//cmk/editions/nonfree:pro",
            "//cmk/editions/nonfree:ultimate",
            "//cmk/editions/nonfree:ultimatemt",
            "//non-free/packages/cmc-protocols:py_config_proto",
            "//non-free/packages/cmc-protocols:py_cycletime_proto",
            "//non-free/packages/cmc-protocols:py_state_proto",
            "//non-free/packages/cmk-mknotifyd",
            "//tests/testlib/unit:unit_nonfree",
        ],
        "@//:gpl_repo": [],
    }),
)
