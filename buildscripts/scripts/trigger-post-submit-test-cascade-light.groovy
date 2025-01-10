#!groovy

/// file: trigger-post-submit-test-cascade-light.groovy

/// Trigger post submit test cascade of lightweight jobs

def main() {
    def package_helper = load("${checkout_dir}/buildscripts/scripts/utils/package_helper.groovy");

    /// This will get us the location to e.g. "checkmk/master" or "Testing/<name>/checkmk/master"
    def branch_base_folder = package_helper.branch_base_folder(with_testing_prefix: true);

    def all_lightweight_jobs = [
        "test-python3-pylint",
        "test-python3-ruff",
        "test-python3-bandit",
        "test-agent-plugin-unit",
        "test-python3-code-quality",
        "test-python3-format",
        "test-python3-typing",
        "test-bazel-lint",
        "test-bazel-format",
        "test-groovy-lint",
        "test-shellcheck_agents",
        "test-shell_format",
        "test-shell-unit",
        "test-python3-unit-all",
    ];

    print(
        """
        |===== CONFIGURATION ===============================
        |all_lightweight_jobs:..... │${all_lightweight_jobs}│
        |checkout_dir:............. │${checkout_dir}│
        |===================================================
        """.stripMargin());

    def build_for_parallel = [:];

    all_lightweight_jobs.each { item ->
        build_for_parallel[item] = { ->
            stage(item) {
                build(
                    job: "${branch_base_folder}/${item}",
                    propagate: true,  // Raise any errors
                    parameters: [
                        string(name: "CUSTOM_GIT_REF", value: effective_git_ref),
                        string(name: "CIPARAM_OVERRIDE_BUILD_NODE", value: CIPARAM_OVERRIDE_BUILD_NODE),
                        string(name: "CIPARAM_CLEANUP_WORKSPACE", value: CIPARAM_CLEANUP_WORKSPACE),
                        string(name: "CIPARAM_BISECT_COMMENT", value: CIPARAM_BISECT_COMMENT),
                    ],
                );
            }
        }
    }

    stage('Trigger all lightweight tests') {
        parallel build_for_parallel;
    }
}

return this;
