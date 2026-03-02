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
        "//cmk/base:cmk_base",
        "//cmk/checkengine:cmk_checkengine",
        "//cmk/utils:cmk_utils",
        "//packages/cmk-livestatus-client:py_livestatus",
        "//packages/cmk-plugin-apis:agent_based",
        "//tests:testlib",
        requirement("fakeredis"),
        requirement("pytest_metadata"),
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
    name = "cmk_gui",
    # https://bazel.build/reference/be/common-definitions#test.size
    size = "large",
    srcs = ["__test__.py"] + glob(
        include = ["cmk/gui/**/*.py"],
        exclude = [
            "**/nonfree/**",
            "**/community/**",
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
        "//cmk/bi:cmk_bi",
        "//cmk/gui:cmk_gui",
        "//omd/packages/omd:omdlib",
        "//tests/testlib/unit:unit_free",
    ],
)

py_test(
    name = "cmk_gui_pro",
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
        "//cmk/utils:cmk_utils",
        "//tests/testlib/unit:unit_free",
        "//tests/unit:cmk_gui",
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
            "//cmk/gui:cmk_gui_pro",
            "//tests/testlib/unit:unit_nonfree",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "cmk_gui_cloud",
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
        "//cmk/gui:cmk_gui",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:user",
        "//packages/cmk-ccc:version",
        "//tests/unit:cmk_gui",
        requirement("pytest"),
        requirement("pytest-mock"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
        requirement("requests"),
        requirement("responses"),
        requirement("werkzeug"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/gui:cmk_gui_cloud",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "cmk_gui_ultimate",
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
        "//cmk/gui:cmk_gui",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:site",
        "//tests/testlib/unit:unit_free",
        "//tests/unit:cmk_gui",
        requirement("python-dateutil"),
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/gui:cmk_gui_ultimate",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "cmk_gui_ultimatemt",
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
        "//tests/testlib/unit:unit_free",
        "//tests/unit:cmk_gui",
        requirement("pytest"),
        requirement("pytest-asyncio"),
        requirement("pytest-random-order"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/gui:cmk_gui_ultimatemt",
        ],
        "@//:gpl_repo": [],
    }),
)

py_test(
    name = "repo",
    # https://bazel.build/reference/be/common-definitions#test.size
    size = "large",
    srcs = ["__test__.py"] + glob(
        include = ["**/*.py"],
        exclude = [
            "omdlib/**/*.py",
            "cmk/gui/**/*.py",
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
        "//cmk:cmk_community",
        "//omd/packages/omd:omdlib",
        "//tests/testlib/unit:unit_free",
        "//tests/unit:conftest",
    ] + select({
        "@//:gpl+nonfree_repo": [
            requirement("python-multipart"),
            "//cmk:cmk_cloud",
            "//cmk:cmk_pro",
            "//cmk:cmk_ultimate",
            "//cmk:cmk_ultimatemt",
            "//non-free/packages/cmc-protocols:py_config_proto",
            "//non-free/packages/cmc-protocols:py_cycletime_proto",
            "//non-free/packages/cmc-protocols:py_state_proto",
            "//non-free/packages/cmk-mknotifyd",
            "//tests/testlib/unit:unit_nonfree",
        ],
        "@//:gpl_repo": [],
    }),
)
