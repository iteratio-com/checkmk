load("@aspect_rules_py//py:defs.bzl", "py_library")
load("//bazel/rules:doctest.bzl", "py_doc_test")

py_library(
    name = "community",
    srcs = [],
    visibility = ["//:__subpackages__"],
    deps = [
        "//cmk",
    ],
)

py_doc_test(
    name = "doctest",
    srcs = [
        ":community",
    ],
    env = {
        "PYTHONWARNINGS": "ignore",
    },
    tags = [
        "doctest",
        "no-mypy",
    ],
)
