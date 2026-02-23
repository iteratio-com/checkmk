"""Bazel rule for running shunit2 shell unit tests."""

def _shunit2_test_impl(ctx):
    # Wrapper design notes:
    # - UNIT_SH_REPO_PATH needs real files (not symlinks): GNU grep -r skips
    #   symlinked files. We resolve via readlink -f on the test script symlink.
    # - The test script is exec'd directly (not `bash script.sh`) so that
    #   ps shows the full `/bin/bash` path; some tests assert CURRENT_SHELL.
    # - HOME is exported to satisfy `set -u` in sourced scripts; tests that
    #   need a writable HOME override it themselves.
    # - env values are Bash expressions evaluated at runtime; Starlark's
    #   str.format() is safe to use here since it doesn't re-parse ${...}.

    wrapper = ctx.actions.declare_file(ctx.label.name + "_shunit2_wrapper.sh")
    ctx.actions.write(
        output = wrapper,
        content = """#!/usr/bin/env bash
# Wrapper for shunit2 test

# Resolve the runfiles directory. Bazel sets RUNFILES_DIR for tests.
if [[ -n "${{RUNFILES_DIR:-}}" ]]; then
    _runfiles="${{RUNFILES_DIR}}"
elif [[ -f "${{BASH_SOURCE[0]}}.runfiles_manifest" ]]; then
    _runfiles="${{BASH_SOURCE[0]}}.runfiles"
else
    _runfiles="${{BASH_SOURCE[0]}}.runfiles"
fi

# Ensure HOME is set; some sourced scripts use it with set -euo pipefail.
export HOME="${{HOME:-${{TEST_TMPDIR:-/tmp}}}}"

# Determine the real workspace root via the test script (always in _main).
_test_in_runfiles="${{_runfiles}}/_main/{test_path}"
if [[ -L "${{_test_in_runfiles}}" ]]; then
    _resolved="$(readlink -f "${{_test_in_runfiles}}")"
    UNIT_SH_REPO_PATH="${{_resolved%/{test_path}}}"
else
    UNIT_SH_REPO_PATH="${{_runfiles}}/_main"
fi

# Resolve shunit2's real path (may be in an external repo).
_shunit2_in_runfiles="${{_runfiles}}/_main/{shunit2_path}"
if [[ -L "${{_shunit2_in_runfiles}}" ]]; then
    UNIT_SH_SHUNIT2="$(readlink -f "${{_shunit2_in_runfiles}}")"
else
    UNIT_SH_SHUNIT2="${{_shunit2_in_runfiles}}"
fi

export UNIT_SH_REPO_PATH
export UNIT_SH_SHUNIT2
{env_exports}
exec "${{_runfiles}}/_main/{test_path}"
        """.format(
            shunit2_path = ctx.files.shunit2[0].short_path,
            test_path = ctx.file.src.short_path,
            env_exports = "".join([
                "export {}=\"{}\"\n".format(key, value)
                for key, value in ctx.attr.env.items()
            ]),
        ),
        is_executable = True,
    )

    runfiles = ctx.runfiles(files = [ctx.file.src, ctx.files.shunit2[0]])
    runfiles = runfiles.merge(ctx.runfiles(files = ctx.files.data))
    for dep in ctx.attr.deps:
        runfiles = runfiles.merge(dep[DefaultInfo].default_runfiles)

    return [DefaultInfo(
        executable = wrapper,
        runfiles = runfiles,
    )]

_shunit2_test = rule(
    implementation = _shunit2_test_impl,
    test = True,
    attrs = {
        "data": attr.label_list(
            doc = "Additional data files available at runtime.",
            allow_files = True,
        ),
        "deps": attr.label_list(
            doc = "Shell library dependencies (sh_library targets) whose files are made available in the runfiles tree.",
            providers = [DefaultInfo],
        ),
        "env": attr.string_dict(
            doc = """Additional environment variables exported before the test runs.

Values are Bash expressions evaluated at runtime, so they may reference
variables already set by the wrapper—in particular ${UNIT_SH_REPO_PATH}.
Example:
    env = {
        "UNIT_SH_AGENTS_DIR":  "${UNIT_SH_REPO_PATH}/agents",
        "UNIT_SH_PLUGINS_DIR": "${UNIT_SH_REPO_PATH}/agents/plugins",
    }
""",
        ),
        "shunit2": attr.label(
            doc = "The shunit2 framework script.",
            default = Label("@shunit2//:shunit2_bin"),
            allow_files = True,
        ),
        "src": attr.label(
            doc = "The shunit2 test script to run.",
            mandatory = True,
            allow_single_file = True,
        ),
    },
)

def shunit2_test(name, src, data = [], deps = [], env = {}, size = "small", tags = [], **kwargs):
    """Run a shunit2 shell unit test under Bazel.

    Args:
        name: The name of the test target.
        src: The shunit2 test script (label or file name).
        data: Additional data files available at runtime.
        deps: Shell library dependencies (sh_library targets) whose source
              files are made available in the runfiles tree.
        env: Additional environment variables to export before the test runs.
             Values are Bash expressions evaluated at runtime and may reference
             ${UNIT_SH_REPO_PATH} (already set by the wrapper).
        size: Test size classification (default: "small").
        tags: Test tags.
        **kwargs: Additional arguments forwarded to the underlying rule
                  (e.g. local = True to disable sandboxing).
    """
    _shunit2_test(
        name = name,
        src = src,
        data = data,
        deps = deps,
        env = env,
        size = size,
        tags = tags,
        **kwargs
    )
