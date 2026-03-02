load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

py_library(
    name = "unit_free",
    testonly = True,
    srcs = glob(
        include = ["**/*.py"],
        exclude = ["**/nonfree/**"],
    ),
    data = glob(
        include = ["**"],
        allow_empty = True,
        exclude = [
            "**/*.py",
            "**/nonfree/**",
        ],
    ),
    imports = ["../../.."],
    visibility = ["//tests:__subpackages__"],
    deps = [
        "//cmk/base:cmk_base",
        "//cmk/gui:cmk_gui",
        "//packages/cmk-ccc:crash-reporting",
        "//tests/testlib/common",
        requirement("flask"),
        requirement("pytest-mock"),
        requirement("pytest"),
        requirement("werkzeug"),
    ],
)

py_library(
    name = "unit_nonfree",
    srcs = glob(
        include = ["**/nonfree/**/*.py"],
        allow_empty = True,
    ),
    data = glob(
        include = ["**"],
        allow_empty = True,
        exclude = ["**/*.py"],
    ),
    imports = ["../../.."],
    target_compatible_with = select({
        "@//:gpl+nonfree_repo": [],
        "@//:gpl_repo": ["@platforms//:incompatible"],
    }),
    visibility = ["//tests:__subpackages__"],
    deps = [
        "//cmk/utils:cmk_utils",
        "//cmk/utils:cmk_utils_pro",
        "//packages/cmk-crypto",
        requirement("requests"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/nonfree/pro/dcd",
        ],
        "@//:gpl_repo": [],
    }),
)
