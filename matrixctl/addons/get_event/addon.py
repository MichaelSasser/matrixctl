#!/usr/bin/env python
# matrixctl
# Copyright (c) 2020  Michael Sasser <Michael@MichaelSasser.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Use this module to get an event from the Database."""

from __future__ import annotations

import json
import logging

from argparse import Namespace

import psycopg

from matrixctl.handlers.db import DBConnectionBuilder
from matrixctl.handlers.ssh_tunnel import ssh_tunnel
from matrixctl.handlers.yaml import YAML
from matrixctl.sanitizers import sanitize_event_identifier


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)

JID_EXT: str = "matrix-jitsi-web"


def addon(arg: Namespace, yaml: YAML) -> int:
    """Get an Event from the Server.

    It connects via paramiko to the server and runs the psql command provided
    by the synapse playbook to run a query on the Database.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``
    yaml : matrixctl.handlers.yaml.YAML
        The configuration file handler.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """

    if not sanitize_event_identifier(arg.event_id):
        return 1

    address = (
        yaml.get("server", "ssh", "address")
        if yaml.get("server", "ssh", "address")
        else f"matrix.{yaml.get('server', 'api', 'domain')}"
    )

    with ssh_tunnel(
        host=address,
        port=int(yaml.get("server", "ssh", "port")),
        username=yaml.get("server", "ssh", "user"),
        remote_port=yaml.get("server", "database", "port"),
        enabled=yaml.get("server", "database", "tunnel"),
        private_key=None,  # TODO yaml.get("server", "database", "private_key")
    ) as tunnel:
        database_port = None
        if tunnel:
            database_port = tunnel.local_bind_port

        connection_uri = DBConnectionBuilder(
            host=(
                "127.0.0.1"
                if yaml.get("server", "database", "tunnel")
                else address
            ),
            port=int(
                database_port or yaml.get("server", "database", "port")
                if yaml.get("server", "database", "tunnel")
                else yaml.get("server", "database", "port")
            ),
            username=yaml.get("server", "database", "synapse_user"),
            password=yaml.get("server", "database", "synapse_password"),
            database=yaml.get("server", "database", "synapse_database"),
        )
        with psycopg.connect(str(connection_uri)) as conn:
            with conn.cursor() as cur:

                cur.execute(
                    "SELECT json FROM event_json WHERE event_id=(%s)",
                    (str(arg.event_id),),
                )
                response = cur.fetchone()[0]
    print(response)
    try:
        print(json.dumps(json.loads(response), indent=4))
    except json.decoder.JSONDecodeError:
        logger.error("Unable to process the response data to JSON.")
        return 1
    return 0


# vim: set ft=python :
