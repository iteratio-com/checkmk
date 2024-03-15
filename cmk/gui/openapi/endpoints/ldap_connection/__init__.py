#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""LDAP Connections"""

from collections.abc import Mapping
from typing import Any

from cmk.gui.fields.custom_fields import LDAPConnectionID
from cmk.gui.http import Response
from cmk.gui.logged_in import user
from cmk.gui.openapi.endpoints.ldap_connection.error_schemas import GETLdapConnection404
from cmk.gui.openapi.endpoints.ldap_connection.internal_to_restapi_interface import (
    LDAPConnectionInterface,
    request_ldap_connection,
    request_ldap_connections,
)
from cmk.gui.openapi.endpoints.ldap_connection.response_schemas import (
    LDAPConnectionResponse,
    LDAPConnectionResponseCollection,
)
from cmk.gui.openapi.restful_objects import Endpoint
from cmk.gui.openapi.restful_objects.constructors import (
    collection_href,
    collection_object,
    domain_object,
    object_href,
    response_with_etag_created_from_dict,
)
from cmk.gui.openapi.restful_objects.registry import EndpointRegistry
from cmk.gui.openapi.restful_objects.type_defs import DomainObject
from cmk.gui.openapi.utils import serve_json
from cmk.gui.utils import permission_verification as permissions

RO_PERMISSIONS = permissions.AllPerm(
    [
        permissions.Perm("wato.seeall"),
        permissions.Perm("wato.users"),
    ]
)
RW_PERMISSIONS = permissions.AllPerm(
    [
        permissions.Perm("wato.edit"),
        RO_PERMISSIONS,
    ]
)


LDAP_CONNECTION_ID_EXISTS = {
    "ldap_connection_id": LDAPConnectionID(presence="should_exist"),
}


@Endpoint(
    object_href("ldap_connection", "{ldap_connection_id}"),
    "cmk/show",
    method="get",
    etag="output",
    tag_group="Setup",
    path_params=[LDAP_CONNECTION_ID_EXISTS],
    response_schema=LDAPConnectionResponse,
    error_schemas={404: GETLdapConnection404},
    permissions_required=RO_PERMISSIONS,
)
def show_ldap_connection(params: Mapping[str, Any]) -> Response:
    """Show an LDAP connection"""
    user.need_permission("wato.seeall")
    user.need_permission("wato.users")
    ldap_id = params["ldap_connection_id"]
    connection = request_ldap_connection(ldap_id=ldap_id)
    return response_with_etag_created_from_dict(
        serve_json(
            _serialize_ldap_connection(
                request_ldap_connection(ldap_id=params["ldap_connection_id"])
            )
        ),
        connection.api_response(),
    )


@Endpoint(
    collection_href("ldap_connection"),
    ".../collection",
    method="get",
    tag_group="Setup",
    response_schema=LDAPConnectionResponseCollection,
    permissions_required=RO_PERMISSIONS,
)
def show_ldap_connections(params: Mapping[str, Any]) -> Response:
    """Show all LDAP connections"""
    user.need_permission("wato.seeall")
    user.need_permission("wato.users")
    return serve_json(
        collection_object(
            domain_type="ldap_connection",
            value=[_serialize_ldap_connection(cnx) for cnx in request_ldap_connections().values()],
        )
    )


def _serialize_ldap_connection(connection: LDAPConnectionInterface) -> DomainObject:
    return domain_object(
        domain_type="ldap_connection",
        identifier=connection.general_properties.id,
        title=connection.general_properties.description,
        extensions=connection.api_response(),
        editable=True,
        deletable=True,
    )


def register(endpoint_registry: EndpointRegistry) -> None:
    endpoint_registry.register(show_ldap_connection)
    endpoint_registry.register(show_ldap_connections)
