load("@aspect_rules_py//py:defs.bzl", "py_library")

py_library(
    name = "cmk_post_rename_site",
    srcs = glob(
        include = ["**/*.py"],
        exclude = [
            "**/community/**",
            "**/nonfree/**",
        ],
    ),
    imports = ["../.."],
    visibility = [
        "//cmk:__subpackages__",
        "//tests:__subpackages__",
    ],
    deps = [
        "//cmk/gui",
        "//cmk/utils",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:i18n",
        "//packages/cmk-ccc:plugin-registry",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:tty",
        "//packages/cmk-ccc:version",
    ],
)

py_library(
    name = "cmk_post_rename_site_pro",
    srcs = glob(
        include = ["**/nonfree/**/pro/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    visibility = [
        "//cmk:__subpackages__",
        "//tests:__subpackages__",
    ],
    deps = [
        ":cmk_post_rename_site",
        "//cmk/gui:pro",
    ],
)

py_library(
    name = "cmk_post_rename_site_ultimate",
    srcs = glob(
        include = ["**/nonfree/**/ultimate/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    visibility = ["//cmk:__subpackages__"],
    deps = [
        ":cmk_post_rename_site",
        "//cmk/gui:ultimate",
    ],
)
