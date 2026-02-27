load("@aspect_rules_py//py:defs.bzl", "py_library")
load("@cmk_requirements//:requirements.bzl", "requirement")

package(default_visibility = [
    "//cmk:__pkg__",
])

py_library(
    name = "cmk_plugins",
    srcs = glob(
        include = ["**/*.py"],
        exclude = [
            "**/community/**",
            "**/nonfree/**",
            "logwatch/**",  # has cmk.base dependencies, see cmk_plugins_logwatch_srcs
        ],
    ),
    imports = ["../.."],
    visibility = [
        "//cmk:__pkg__",
        "//cmk/legacy_checks:__pkg__",
        "//cmk/legacy_includes:__pkg__",
    ],
    deps = [
        "//cmk/bi:cmk_bi",
        "//cmk/utils:cmk_utils",
        "//packages/cmk-ccc:debug",
        "//packages/cmk-ccc:exceptions",
        "//packages/cmk-ccc:hostaddress",
        "//packages/cmk-ccc:i18n",
        "//packages/cmk-ccc:plugin-registry",
        "//packages/cmk-ccc:regex",
        "//packages/cmk-ccc:site",
        "//packages/cmk-ccc:store",
        "//packages/cmk-ccc:version",
        "//packages/cmk-crypto",
        "//packages/cmk-ec:event",
        "//packages/cmk-ec:syslog",
        "//packages/cmk-events",
        "//packages/cmk-livestatus-client:py_livestatus",
        "//packages/cmk-plugin-apis:agent_based",
        "//packages/cmk-plugin-apis:bakery",
        "//packages/cmk-plugin-apis:discover_plugins",
        "//packages/cmk-plugin-apis:graphing",
        "//packages/cmk-plugin-apis:inventory_ui",
        "//packages/cmk-plugin-apis:password_store",
        "//packages/cmk-plugin-apis:rulesets",
        "//packages/cmk-plugin-apis:server_side_calls",
        "//packages/cmk-plugin-apis:server_side_programs",
        "//packages/cmk-plugins:lib",
        "//packages/cmk-werks",
        requirement("boto3"),
        requirement("botocore"),
        requirement("cryptography"),
        requirement("exchangelib"),  # missing wheel
        requirement("feedparser"),
        requirement("google-api-python-client"),
        requirement("google-auth"),
        requirement("google-cloud-asset"),
        requirement("google-cloud-monitoring"),
        requirement("jira"),
        requirement("lxml"),
        requirement("meraki"),
        requirement("msal"),
        requirement("mypy-boto3-logs"),
        requirement("oauthlib"),
        requirement("paho-mqtt"),
        requirement("paramiko"),
        requirement("protobuf"),
        requirement("psycopg2-binary"),  # missing wheel
        requirement("pyasn1"),
        requirement("pydantic"),
        requirement("pymongo"),
        requirement("pymssql"),
        requirement("pymysql"),
        requirement("pyopenssl"),
        requirement("pysmb"),
        requirement("python-dateutil"),
        requirement("python-snap7"),
        requirement("pyyaml"),
        requirement("requests"),
        requirement("requests-oauthlib"),
    ],
)

# Logwatch has cmk.base dependencies - its sources are added directly to cmk_cmk
# rather than being a separate py_library, so type checking happens with cmk.base available.
#
# We accept this hack to be able to extract thousands of files from the monolithic cmk_cmk
# target now, which enables way faster lint and test runs. The next step is to extract all
# families to packages/cmk-plugins, which then results in the current target state.
filegroup(
    name = "cmk_plugins_logwatch_srcs",
    srcs = glob(["logwatch/**/*.py"]),
)

# Robotmk nonfree files import from cmk.nonfree.pro.robotmk.* - their sources are added
# directly to cmk_pro so type checking happens with the nonfree packages available.
filegroup(
    name = "cmk_plugins_robotmk_nonfree_srcs",
    srcs = glob(
        ["robotmk/**/nonfree/**/*.py"],
        allow_empty = True,
    ),
)

# Otel and custom_query_metric_backend nonfree files import from cmk.metric_backend.*,
# cmk.otel_collector.*, etc. - their sources are added directly to cmk_ultimate
# so type checking happens with the nonfree packages available.
#
# We accept this hack to be able to extract thousands of files from the monolithic cmk_cmk
# target now, which enables way faster lint and test runs. The next step is to extract all
# families to packages/cmk-plugins, which then results in the current target state.
filegroup(
    name = "cmk_plugins_otel_nonfree_srcs",
    srcs = glob(
        [
            "otel/**/nonfree/**/*.py",
            "custom_query_metric_backend/**/nonfree/**/*.py",
        ],
        allow_empty = True,
    ),
)

py_library(
    name = "cmk_plugins_community",
    srcs = glob(
        include = ["**/community/**/*.py"],
        allow_empty = True,
        exclude = ["**/nonfree/**"],
    ),
    imports = ["../.."],
    deps = [":cmk_plugins"],
)

py_library(
    name = "cmk_plugins_pro",
    srcs = glob(
        include = [
            "**/nonfree/**/pro/**/*.py",
            "**/nonfree/**/*.py",
        ],
        allow_empty = True,
        exclude = [
            "**/nonfree/**/cloud/**",
            "**/nonfree/**/ultimate/**",
            "**/nonfree/**/ultimatemt/**",
            # Exclude robotmk nonfree files - they import from cmk.nonfree.pro.robotmk.*
            # which lives in cmk/nonfree/pro/robotmk/ and is part of //cmk:cmk_pro
            "robotmk/**/nonfree/**",
        ],
    ),
    imports = ["../.."],
    deps = [
        ":cmk_plugins",
        ":cmk_plugins_community",
        requirement("robotframework"),
    ] + select({
        "@//:gpl+nonfree_repo": [
            "//cmk/nonfree/pro/robotmk",
            "//cmk/nonfree/pro/robotmk:bakery",
        ],
        "@//:gpl_repo": [],
    }),
)

py_library(
    name = "cmk_plugins_ultimate",
    srcs = glob(
        include = ["**/nonfree/**/ultimate/**/*.py"],
        allow_empty = True,
        exclude = [
            # Exclude otel and custom_query_metric_backend nonfree files - they import from
            # cmk.metric_backend.*, cmk.otel_collector.*, etc. which are in //cmk:cmk_ultimate
            "otel/**/nonfree/**",
            "custom_query_metric_backend/**/nonfree/**",
        ],
    ),
    imports = ["../.."],
    deps = [
        ":cmk_plugins",
        ":cmk_plugins_community",
        ":cmk_plugins_pro",
    ],
)

py_library(
    name = "cmk_plugins_cloud",
    srcs = glob(
        include = ["**/nonfree/**/cloud/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    deps = [
        ":cmk_plugins",
        ":cmk_plugins_community",
        ":cmk_plugins_pro",
        ":cmk_plugins_ultimate",
    ],
)

py_library(
    name = "cmk_plugins_ultimatemt",
    srcs = glob(
        include = ["**/nonfree/**/ultimatemt/**/*.py"],
        allow_empty = True,
    ),
    imports = ["../.."],
    deps = [
        ":cmk_plugins",
        ":cmk_plugins_community",
        ":cmk_plugins_pro",
        ":cmk_plugins_ultimate",
    ],
)

filegroup(
    name = "checkman_community",
    srcs = glob(
        ["**/checkman/**"],
        exclude = [
            "**/OWNERS",
            "**/checkman/nonfree/**",
        ],
    ),
)

filegroup(
    name = "checkman_pro",
    srcs = glob(
        ["**/checkman/nonfree/pro/**"],
        allow_empty = True,
        exclude = ["**/OWNERS"],
    ) + [
        ":checkman_community",
    ],
)

filegroup(
    name = "checkman_ultimate",
    srcs = glob(
        ["**/checkman/nonfree/ultimate/**"],
        allow_empty = True,
        exclude = ["**/OWNERS"],
    ) + [
        ":checkman_community",
        ":checkman_pro",
    ],
)

filegroup(
    name = "checkman_cloud",
    srcs = glob(
        ["**/checkman/nonfree/cloud/**"],
        allow_empty = True,
        exclude = ["**/OWNERS"],
    ) + [
        ":checkman_community",
        ":checkman_pro",
        ":checkman_ultimate",
    ],
)

filegroup(
    name = "checkman_ultimatemt",
    srcs = glob(
        ["**/checkman/nonfree/ultimatemt/**"],
        allow_empty = True,
        exclude = ["**/OWNERS"],
    ) + [
        ":checkman_community",
        ":checkman_pro",
        ":checkman_ultimate",
    ],
)

filegroup(
    name = "agents",
    srcs = glob(
        include = ["**/agents/**/*"],
        exclude = ["**/agents/**/*.py"],
    ),
)

filegroup(
    name = "libexec",
    srcs = glob(
        [
            "**/libexec/*",
        ],
    ),
    visibility = ["//omd:__subpackages__"],
)

filegroup(
    name = "shell_scripts",
    srcs = [
        "activemq/libexec/agent_activemq",
        "alertmanager/libexec/agent_alertmanager",
        "allnet_ip_sensoric/libexec/agent_allnet_ip_sensoric",
        "appdynamics/libexec/agent_appdynamics",
        "azure_deprecated/libexec/agent_azure",
        "azure_status/libexec/agent_azure_status",
        "azure_v2/libexec/agent_azure_v2",
        "bazel/libexec/agent_bazel_cache",
        "checkmk/libexec/agent_bi",
        "checkmk/libexec/check_cmk_inv",
        "cisco_meraki/libexec/agent_cisco_meraki",
        "couchbase/libexec/agent_couchbase",
        "datadog/libexec/agent_datadog",
        "ddn_s2a/libexec/agent_ddn_s2a",
        "emailchecks/libexec/check_mail",
        "emailchecks/libexec/check_mail_loop",
        "emailchecks/libexec/check_mailboxes",
        "form_submit/libexec/check_form_submit",
        "fritzbox/libexec/agent_fritzbox",
        "gcp/libexec/agent_gcp",
        "gcp/libexec/agent_gcp_status",
        "gerrit/libexec/agent_gerrit",
        "hivemanager/libexec/agent_hivemanager",
        "hivemanager_ng/libexec/agent_hivemanager_ng",
        "hp_msa/libexec/agent_hp_msa",
        "hpe_3par/libexec/agent_three_par",
        "ibmsvc/libexec/agent_ibmsvc",
        "innovaphone/libexec/agent_innovaphone",
        "jenkins/libexec/agent_jenkins",
        "jira/libexec/agent_jira",
        "jolokia/libexec/agent_jolokia",
        "mobileiron/libexec/agent_mobileiron",
        "mqtt/libexec/agent_mqtt",
        "oracle/.f12",
        "oracle/agents/oracle_unified_async",
        "oracle/agents/oracle_unified_sync",
        "prometheus/libexec/agent_prometheus",
        "ruckus_spot/libexec/agent_ruckus_spot",
        "salesforce/libexec/agent_salesforce",
        "sftp/libexec/check_sftp",
        "siemens_plc/libexec/agent_siemens_plc",
        "smb/libexec/agent_smb_share",
        "smb/libexec/check_disk_smb",
        "sql/libexec/check_sql",
        "storeonce/libexec/agent_storeonce",
        "storeonce4x/libexec/agent_storeonce4x",
        "tinkerforge/libexec/agent_tinkerforge",
        "traceroute/libexec/check_traceroute",
        "uniserv/libexec/check_uniserv",
        "vnx_quotas/libexec/agent_vnx_quotas",
        "zerto/libexec/agent_zerto",
    ],
)
