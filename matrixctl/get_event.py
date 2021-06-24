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

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction
from base64 import b64encode

from .handlers.ssh import SSH
from .handlers.ssh import SSHResponse
from .handlers.toml import TOML
from .typing import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)

JID_EXT: str = "matrix-jitsi-web"


def subparser_get_event(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl get-event`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by
        ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "get-event", help="get an event from the DB"
    )
    parser.add_argument("event_id", help="The event-id")
    parser.set_defaults(func=get_event)


def get_event(arg: Namespace) -> int:
    """Get an Event from the Server.

    It connects via paramiko to the server and runs the psql command provided
    by the synapse playbook to run a query on the Database.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """

    toml: TOML = TOML()
    address = (
        toml.get("SSH", "Address")
        if toml.get("SSH", "Address")
        else f"matrix.{toml.get('API', 'Domain')}"
    )

    # Workaround because of "$" through: paramiko - bash - psql
    event64 = b64encode(arg.event_id.encode("utf-8")).decode("utf-8")

    query: str = "SELECT json FROM event_json WHERE event_id='$event'"
    cmd: str = "/usr/local/bin/matrix-postgres-cli -P pager"
    table: str = "synapse"

    command: str = (
        f"event=$(echo '{event64}' | base64 -d -) && "  # Workaround
        f'sudo {cmd} -d {table} -c "{query}"'
    )

    logger.debug(f"command: {command}")

    with SSH(address, toml.get("SSH", "User"), toml.get("SSH", "Port")) as ssh:
        response: SSHResponse = ssh.run_cmd(command, tty=True)

    if not response.stderr:
        logger.debug(f"response: {response.stdout}")
        if response.stdout:
            start: int = response.stdout.find("{")
            stop: int = response.stdout.rfind("}") + 1

            response_parsed: JsonDict = json.loads(response.stdout[start:stop])
            print(json.dumps(response_parsed, indent=4))
            return 0
        print("The response from the Database was empty.")
        return 0
    logger.error(f"response: {response.stderr}")
    print(
        "An error occured during the query. Are you sure, you used the "
        "correct event_id?"
    )
    return 1


# vim: set ft=python :
