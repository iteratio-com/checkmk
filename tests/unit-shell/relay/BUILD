load("//bazel/rules:shunit2.bzl", "shunit2_test")

sh_library(
    name = "relay_test_helpers",
    srcs = ["mocks.sh"],
)

[
    shunit2_test(
        name = src.replace(".sh", ""),
        src = src,
        deps = [
            ":relay_test_helpers",
            "//omd/non-free/relay:omd_non-free_relay_sh",
        ],
    )
    for src in glob(["test_*.sh"])
]
