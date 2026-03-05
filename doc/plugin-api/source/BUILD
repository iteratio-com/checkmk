load("@aspect_rules_py//py:defs.bzl", "py_binary")
load("@bazel_skylib//rules:build_test.bzl", "build_test")
load("@cmk_requirements//:requirements.bzl", "requirement")
load("@rules_pkg//pkg:tar.bzl", "pkg_tar")
load("@rules_sphinx//sphinx:defs.bzl", "sphinx_html")

py_binary(
    name = "sphinx_build",
    srcs = ["@rules_sphinx//sphinx/tools:sphinx_build_wrapper.py"],
    main = "sphinx_build_wrapper.py",
    tags = ["no-mypy"],
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
        requirement("sphinx"),
        requirement("sphinx_autodoc_typehints"),
        requirement("sphinx_rtd_theme"),
        requirement("pydantic"),
    ],
)

filegroup(
    name = "srcs",
    srcs = glob(
        include = ["**/*.rst"],
        exclude = ["**/nonfree/**"],
    ),
)

filegroup(
    name = "srcs_nonfree",
    srcs = glob(
        include = ["**/nonfree/**/*.rst"],
        allow_empty = True,
    ),
)

sphinx_html(
    name = "plugin-api",
    srcs = glob(["_static/**/*"]) + [":srcs"] + select({
        "@cmk//edition:community": [],
        "//conditions:default": [":srcs_nonfree"],
    }),
    args = ["--fail-on-warning"],
    config = "conf.py",
    index = "index.rst",
    sphinx_build = ":sphinx_build",
)

alias(
    name = "view",
    actual = ":plugin-api.view",
    visibility = ["//:__subpackages__"],
)

build_test(
    name = "build_test",
    targets = [":plugin-api"],
)

pkg_tar(
    name = "pkg_tar",
    srcs = [
        ":plugin-api",
    ],
    package_dir = "share/doc/check_mk/plugin-api/html",
    stamp = 1,
    strip_prefix = "plugin-api_html",
    visibility = ["//omd:__pkg__"],
)
