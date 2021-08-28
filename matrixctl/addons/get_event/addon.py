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
import re

from argparse import Namespace
from base64 import b64encode

from matrixctl.handlers.ssh import SSH
from matrixctl.handlers.ssh import SSHResponse
from matrixctl.handlers.yaml import YAML


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

    address = (
        yaml.get("server", "ssh", "address")
        if yaml.get("server", "ssh", "address")
        else f"matrix.{yaml.get('server', 'api', 'domain')}"
    )

    is_valid_event_id = re.match(r"^\$[0-9a-zA-Z.=_-]{1,255}$", arg.event_id)
    if not is_valid_event_id:
        logger.error(
            "The given event_id has an invalid format. Please make sure you "
            "use one with the correct format. "
            "Example: $tjeDdqYAk9BDLAUcniGUy640e_D9TrWU2RmCksJQQEQ"
        )
        return 1

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

    with SSH(
        address,
        yaml.get("server", "ssh", "user"),
        yaml.get("server", "ssh", "port"),
    ) as ssh:
        response: SSHResponse = ssh.run_cmd(command, tty=True)

    if not response.stderr:
        logger.debug(f"response: {response.stdout}")
        if response.stdout:
            start: int = response.stdout.find("{")
            stop: int = response.stdout.rfind("}") + 1
            logger.debug(f"{start=}, {stop=}")
            if start == -1 and stop == 0:  # "empty" response
                logger.error(
                    "The event_id was not not in the Database. Please check "
                    "if you entered the correct one. "
                )
                return 1
            try:
                print(
                    json.dumps(
                        json.loads(response.stdout[start:stop]), indent=4
                    )
                )
                return 0
            except json.decoder.JSONDecodeError:
                logger.error("Unable to process the response data to JSON.")
                return 1
        print("The response from the Database was empty.")
        return 0
    logger.error(f"response: {response.stderr}")
    print(
        "An error occured during the query. Are you sure, you used the "
        "correct event_id?"
    )
    return 1


# vim: set ft=python :
