#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping
from typing import Any

from cmk.agent_based.v1 import check_levels as check_levels_v1
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    IgnoreResultsError,
    InventoryPlugin,
    InventoryResult,
    Metric,
    render,
    Result,
    Service,
    State,
    StringTable,
    TableRow,
)
from cmk.plugins.lib import db
from cmk.plugins.oracle.agent_based import liboracle as oracle

# no used space check for Tablsspaces with CONTENTS in ('TEMPORARY','UNDO')
# It is impossible to check the used space in UNDO and TEMPORARY Tablespaces
# These Types of Tablespaces are ignored in this plug-in.
# This restriction is only working with newer agents, because we need an
# additional parameter at end if each datafile

ORACLE_TABLESPACES_DEFAULTS = {
    "levels": (10.0, 5.0),
    "magic_normsize": 1000,
    "magic_maxlevels": (60.0, 50.0),
    "defaultincrement": True,
}

# <<<oracle_tablespaces>>>
# pengt /database/pengt/daten155/dbf/system_01.dbf SYSTEM AVAILABLE YES 38400 4194302 38392 1280 SYSTEM 8192 ONLINE
# pengt /database/pengt/daten155/dbf/undotbs_01.dbf UNDOTBS1 AVAILABLE YES 128000 4194302 127992 640 ONLINE 8192 ONLINE
# pengt /database/pengt/daten155/dbf/sysaux_01.dbf SYSAUX AVAILABLE YES 25600 4194302 25592 1280 ONLINE 8192 ONLINE
# pengt /database/pengt/daten155/dbf/ts_user_01.dbf TS_USER AVAILABLE YES 8480 1280000 8472 160 ONLINE 8192 ONLINE
# pengt /database/pengt/daten155/dbf/TS_PENG_ABR_01.dbf TS_PENG_ABR AVAILABLE YES 12800 1280000 12792 12800 ONLINE 8192 ONLINE

# invalid data
# <<<oracle_tablespaces>>>
# AIMCOND1|/u00/app/oracle/product/db12010/dbs/MISSING00064|CONRPG_DATA|AVAILABLE||||||OFFLINE|8192|ONLINE|0|PERMANENT
# MAE|/opt/oracle/oracle_base/product/11.2.0.4/dbs/pslife_dwh.dbf|PSLIFE_DWH|AVAILABLE||||||RECOVER|8192|OFFLINE|0|PERMANENT

# Order of columns (it is a table of data files, so table spaces appear multiple times)
# 0  database SID
# 1  data file name
# 2  table space name
# 3  status of the data file
# 4  whether the file is auto extensible
# 5  current size of data file in blocks
# 6  maximum size of data file in blocks (if auto extensible)
# 7  currently number of blocks used by user data
# 8  size of next increment in blocks (if auto extensible)
# 9  wheter the file is in use (online)
# 10 block size in bytes
# 11 status of the table space
# 12 free space in the datafile
# 13 Tablespace-Type (PERMANENT, UNDO, TEMPORARY)


def parse_oracle_tablespaces(string_table: StringTable) -> oracle.SectionTableSpaces:
    tablespaces: dict[tuple[str, str], oracle.TableSpaces] = {}
    error_sids: oracle.ErrorSids = {}

    for line in string_table:
        # Check for query errors
        check_ora = oracle.OraErrors(line)
        if check_ora.ignore:
            continue  # ignore ancient agent outputs
        if check_ora.has_error:
            sid = line[0]
            error_sids[sid] = check_ora

        if len(line) not in (13, 14, 15):
            continue

        (
            sid,
            datafile_name,
            ts_name,
            datafile_status,
            autoextensible,
            filesize_blocks,
            max_filesize_blocks,
            used_blocks,
            increment_size,
            file_online_status,
            block_size,
            ts_status,
            free_space,
        ) = line[:13]

        db_version = 0

        if len(line) >= 14:
            ts_type = line[13]
        else:
            # old behavior is all Tablespaces are treated as PERMANENT
            ts_type = "PERMANENT"

        if len(line) == 15:
            db_version = int(line[14].split(".")[0])

        tablespaces.setdefault(
            (sid, ts_name),
            {
                "amount_missing_filenames": 0,
                "autoextensible": False,
                "datafiles": [],
                "db_version": db_version,
                "status": ts_status,
                "type": ts_type,
            },
        )

        datafiles: oracle.DataFiles = {
            "name": datafile_name,
            "status": datafile_status,
            "autoextensible": autoextensible == "YES",
            "ts_type": ts_type,
            "ts_status": ts_status,
            "file_online_status": file_online_status,
            "block_size": None,
            "size": None,
            "max_size": None,
            "used_size": None,
            "free_space": None,
            "increment_size": None,
        }

        try:
            bs = int(block_size)
            datafiles.update(
                {
                    "block_size": bs,
                    "size": int(filesize_blocks) * bs,
                    "max_size": int(max_filesize_blocks) * bs,
                    "used_size": int(used_blocks) * bs,
                    "free_space": int(free_space) * bs,
                    "increment_size": int(increment_size) * bs,
                }
            )

        except ValueError:
            pass
        tablespaces[(sid, ts_name)]["datafiles"].append(datafiles)

    for v in tablespaces.values():
        v["amount_missing_filenames"] = len([df for df in v["datafiles"] if df["name"] == ""])
        v["autoextensible"] = any(df["autoextensible"] for df in v["datafiles"])

    return {"error_sids": error_sids, "tablespaces": tablespaces}


agent_section_oracle_tablespaces = AgentSection(
    name="oracle_tablespaces",
    parse_function=parse_oracle_tablespaces,
)


def discovery_oracle_tablespaces(section: oracle.SectionTableSpaces) -> DiscoveryResult:
    for (sid, ts_name), tablespace in section["tablespaces"].items():
        if tablespace["status"] in ("ONLINE", "READONLY", "OFFLINE"):
            yield Service(
                item=f"{sid}.{ts_name}",
                parameters={"autoextend": tablespace["autoextensible"]},
            )


def check_oracle_tablespaces(
    item: str,
    params: Mapping[str, Any],
    section: oracle.SectionTableSpaces,
) -> CheckResult:
    try:
        if item.count(".") == 2:
            # Pluggable Database: item = <CDB>.<PDB>.<Tablespace>
            cdb, pdb, ts_name = item.split(".")
            sid = cdb + "." + pdb
        else:
            sid, ts_name = item.split(".", 1)
    except ValueError:
        yield Result(state=State.UNKNOWN, summary="Invalid check item (must be <SID>.<tablespace>)")
        return

    if sid in section["error_sids"]:
        ora_error = section["error_sids"][sid]
        yield Result(state=ora_error.error_severity, summary=ora_error.error_text)
        return

    # In case of missing information we assume that the login into
    # the database has failed and we simply skip this check. It won't
    # switch to UNKNOWN, but will get stale.
    # TODO Treatment as in db2 and mssql dbs
    # "ts_status is None" possible?
    tablespace = section["tablespaces"].get((sid, ts_name))
    if not tablespace or tablespace["status"] is None:
        raise IgnoreResultsError("Login into database failed")

    ts_type = tablespace["type"]
    ts_status = tablespace["status"]
    db_version = tablespace["db_version"]

    # Conversion of old autochecks params
    if isinstance(params, tuple):
        params = {"autoextend": params[0], "levels": params[1:]}

    autoext = params.get("autoextend", None)
    uses_default_increment = False

    # check for missing filenames in Tablespaces. This is possible after recreation
    # of controlfiles in temporary Tablespaces
    # => CRIT, because we are not able to calculate used/free space in Tablespace
    #          in most cases the temporary Tablespace is empty
    if tablespace["amount_missing_filenames"] > 0:
        yield Result(
            state=State.CRIT,
            summary="%d files with missing filename in %s Tablespace, space calculation not possible"
            % (tablespace["amount_missing_filenames"], ts_type),
        )
        return

    stats = oracle.datafiles_online_stats(tablespace["datafiles"], db_version)

    if stats is not None:
        yield Result(
            state=State.OK,
            summary="%s (%s), Size: %s, %s used (%s of max. %s), Free: %s"
            % (
                ts_status,
                ts_type,
                render.bytes(stats.current_size),
                render.percent(100.0 * stats.used_size / stats.max_size),
                render.bytes(stats.used_size),
                render.bytes(stats.max_size),
                render.bytes(stats.free_space),
            ),
        )

        if stats.num_extensible > 0 and db_version <= 10:
            # only display the number of remaining extents in Databases <= 10g
            yield Result(
                state=State.OK,
                summary="%d increments (%s)"
                % (stats.num_increments, render.bytes(stats.increment_size)),
            )

        if ts_status != "READONLY":
            warn, crit, _as_perc, _info_text = db.get_tablespace_levels_in_bytes(
                stats.max_size, params
            )

            yield Metric(
                name="size",
                value=stats.current_size,
                levels=(stats.max_size - warn, stats.max_size - crit) if warn and crit else None,
                boundaries=(0, stats.max_size),
            )
            yield Metric(
                name="used",
                value=stats.used_size,
            )
            yield Metric(
                name="max_size",
                value=stats.max_size,
            )

            # Check increment size, should not be set to default (1)
            if params.get("defaultincrement"):
                if uses_default_increment:
                    yield Result(state=State.WARN, summary="DEFAULT INCREMENT")

        # Check autoextend status if parameter not set to None
        if autoext is not None and ts_status != "READONLY":
            autoext_info: str | None
            if autoext and stats.num_extensible == 0:
                autoext_info = "NO AUTOEXTEND"
            elif not autoext and stats.num_extensible > 0:
                autoext_info = "AUTOTEXTEND"
            else:
                autoext_info = None

            if autoext_info:
                yield Result(
                    state=State(params.get("autoextend_severity", 2)), summary=autoext_info
                )

        elif stats.num_extensible > 0:
            yield Result(state=State.OK, summary="autoextend")

        else:
            yield Result(state=State.OK, summary="no autoextend")

        # Check free space, but only if status is not READONLY
        # and Tablespace-Type must be PERMANENT or TEMPORARY, when temptablespace is True
        # old plugins without v$tempseg_usage info send TEMP as type.
        # => Impossible to monitor old plug-in with TEMP instead TEMPORARY
        if ts_status != "READONLY" and (
            ts_type == "PERMANENT"
            or (ts_type == "TEMPORARY" and params.get("temptablespace"))
            or (ts_type == "UNDO" and params.get("monitor_undo_tablespace"))
        ):
            yield from check_levels_v1(
                stats.free_space,
                levels_lower=(warn, crit),
                render_func=render.bytes,
                label="Space left",
            )
        if stats.num_files != 1 or stats.num_avail != 1 or stats.num_extensible != 1:
            yield Result(
                state=State.OK,
                summary="%d data files (%d avail, %d autoext)"
                % (stats.num_files, stats.num_avail, stats.num_extensible),
            )

    unavailable = oracle.check_unavailable_datafiles(tablespace["datafiles"])
    unavailable_mapping = dict(params.get("map_file_online_states", []))
    for datafile_status, datafiles in (
        ("OFFLINE", unavailable.offline),
        ("RECOVER", unavailable.recover),
    ):
        if datafiles:
            details = "\n".join(e.name for e in datafiles)
            yield Result(
                state=State(unavailable_mapping.get(datafile_status, State.CRIT)),
                summary=f"Datafiles {datafile_status}: {sid}",
                details=f"{datafile_status} datafiles for {sid}:\n{details}",
            )


def cluster_check_oracle_tablespaces(
    item: str, params: dict[str, Any], section: Mapping[str, oracle.SectionTableSpaces | None]
) -> CheckResult:
    selected_tablespaces: oracle.SectionTableSpaces = {"tablespaces": {}, "error_sids": {}}

    # If there are more than one nodes per tablespace, then we select the node with the
    # most data files
    for tablespaces_per_node in section.values():
        if tablespaces_per_node is None:
            continue

        for (sid, ts_name), tablespace in tablespaces_per_node["tablespaces"].items():
            if (sid, ts_name) not in selected_tablespaces or len(
                selected_tablespaces["tablespaces"][(sid, ts_name)]["datafiles"]
            ) < len(tablespace["datafiles"]):
                selected_tablespaces["tablespaces"][(sid, ts_name)] = tablespace
            selected_tablespaces["error_sids"].update(tablespaces_per_node["error_sids"])

    yield from check_oracle_tablespaces(item, params, selected_tablespaces)


check_plugin_oracle_tablespaces = CheckPlugin(
    name="oracle_tablespaces",
    service_name="ORA %s Tablespace",
    discovery_function=discovery_oracle_tablespaces,
    check_function=check_oracle_tablespaces,
    check_default_parameters=ORACLE_TABLESPACES_DEFAULTS,
    check_ruleset_name="oracle_tablespaces",
    cluster_check_function=cluster_check_oracle_tablespaces,
)

# AIMSTGD1|/u01/oradata/aimstgd1/temp0104.dbf|TEMP01|ONLINE|YES|90112|3276800|90048|8192|TEMP|32768|ONLINE|0|TEMPORARY
# AIMSTGD1|/u01/oradata/aimstgd1/temp0105.dbf|TEMP01|ONLINE|YES|90112|3276800|90048|8192|TEMP|32768|ONLINE|0|TEMPORARY
# AIMSTGD1|/u01/oradata/aimstgd1/temp0106.dbf|TEMP01|ONLINE|YES|90112|3276800|90048|8192|TEMP|32768|ONLINE|4544|TEMPORARY
# AIMCONS1|/u01/oradata/aimcons1/temp01.dbf|TEMP|ONLINE|YES|262144|2621440|262016|32768|TEMP|8192|ONLINE|258560|TEMPORARY
# AIMCONS1|/u01/oradata/aimcons1/temp02.dbf|TEMP|ONLINE|YES|262144|2621440|262016|32768|TEMP|8192|ONLINE|258688|TEMPORARY

# Order of columns (it is a table of data files, so table spaces appear multiple times)
# 0  database SID
# 1  data file name
# 2  table space name
# 3  status of the data file
# 4  whether the file is auto extensible
# 5  current size of data file in blocks
# 6  maximum size of data file in blocks (if auto extensible)
# 7  currently number of blocks used by user data
# 8  size of next increment in blocks (if auto extensible)
# 9  wheter the file is in use (online)
# 10 block size in bytes
# 11 status of the table space
# 12 free space in the datafile
# 13 Tablespace-Type (PERMANENT, UNDO, TEMPORARY)


def inventory_oracle_tablespaces(section: oracle.SectionTableSpaces) -> InventoryResult:
    tablespaces = section["tablespaces"]
    for tablespace in tablespaces:
        sid, name = tablespace
        attrs = tablespaces[tablespace]
        db_version = attrs["db_version"]

        stats = oracle.datafiles_online_stats(
            attrs["datafiles"],
            db_version,
        )

        status_columns = None
        if stats is not None:
            status_columns = {
                "current_size": stats.current_size,
                "max_size": stats.max_size,
                "used_size": stats.used_size,
                "num_increments": stats.num_increments,
                "increment_size": stats.increment_size,
                "free_space": stats.free_space,
            }

        yield TableRow(
            path=["software", "applications", "oracle", "tablespaces"],
            key_columns={
                "sid": sid,
                "name": name,
            },
            inventory_columns={
                "version": db_version or "",
                "type": attrs["type"],
                "autoextensible": attrs["autoextensible"] and "YES" or "NO",
            },
            status_columns=status_columns,
        )


inventory_plugin_oracle_tablespaces = InventoryPlugin(
    name="oracle_tablespaces",
    inventory_function=inventory_oracle_tablespaces,
    sections=["oracle_tablespaces"],
)
