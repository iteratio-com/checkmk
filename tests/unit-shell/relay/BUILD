load("//bazel/rules:shunit2.bzl", "shunit2_test")

sh_library(
    name = "relay_test_helpers",
    srcs = ["mocks.sh"],
)

[
    shunit2_test(
        name = src.replace(".sh", ""),
        src = src,
        target_compatible_with = select({
            "@//:gpl+nonfree_repo": [],
            "@//:gpl_repo": ["@platforms//:incompatible"],
        }),
        deps = [
            ":relay_test_helpers",
        ] + select({
            "@//:gpl+nonfree_repo": [
                "//omd/non-free/relay:omd_non-free_relay_sh",
            ],
            "@//:gpl_repo": [],
        }),
    )
    for src in glob(["test_*.sh"])
]
