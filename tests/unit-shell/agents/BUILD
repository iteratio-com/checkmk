load("//bazel/rules:shunit2.bzl", "shunit2_test")

[
    shunit2_test(
        name = src.replace(".sh", ""),
        src = src,
        env = {
            "UNIT_SH_AGENTS_DIR": "${UNIT_SH_REPO_PATH}/agents",
            "UNIT_SH_PLUGINS_DIR": "${UNIT_SH_REPO_PATH}/agents/plugins",
        },
        deps = ["//agents:agents_sh"],
    )
    for src in glob(["test_*.sh"])
    if src != "test_mk-job.sh"
]

# test_mk-job uses cleanup_running_files which inspects /proc/<pid>/cmdline.
# In Bazel's linux-sandbox the sandbox-init process (PID 1) has the test name
# in its command line, causing a false "mk-job" match that breaks the cleanup
# assertion. Running this test locally (no sandbox) avoids the issue.
shunit2_test(
    name = "test_mk-job",
    src = "test_mk-job.sh",
    env = {
        "UNIT_SH_AGENTS_DIR": "${UNIT_SH_REPO_PATH}/agents",
        "UNIT_SH_PLUGINS_DIR": "${UNIT_SH_REPO_PATH}/agents/plugins",
    },
    local = True,
    deps = ["//agents:agents_sh"],
)
