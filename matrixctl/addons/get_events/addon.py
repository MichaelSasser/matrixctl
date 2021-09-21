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
import sys

from argparse import Namespace
from contextlib import suppress
from enum import Enum
from enum import unique
from typing import Match

from matrixctl.handlers.ssh import SSH
from matrixctl.handlers.ssh import SSHResponse
from matrixctl.handlers.yaml import YAML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


@unique
class MessageType(Enum):

    """Use this enum for describing message types.

    Supported events:

    ===================== ===================================================
    message_type          Usage
    ===================== ===================================================
    m.room.message        This event is used when sending messages in a room
    m.room.name           This event sets the name of an room
    m.room.topic          This events sets the room topic
    m.room.avatar         This event sets the room avatar
    m.room.pinned_events  This event pins events
    m.room.member         Adjusts the membership state for a user in a room
    m.room.join_rules     This event sets the join rules
    m.room.create         This event creates a room
    m.room.power_levels   This event sets a rooms power levels
    m.room.redaction      This event redacts other events
    ===================== ===================================================

    """

    M_ROOM_MESSAGE = "m.room.message"
    M_ROOM_NAME = "m.room.name"
    M_ROOM_TOPIC = "m.room.topic"
    M_ROOM_AVATAR = "m.room.avatar"
    M_ROOM_PINNED_EVENTS = "m.room.pinned_events"
    M_ROOM_MEMBER = "m.room.member"
    M_ROOM_JOIN_RULES = "m.room.join_rules"
    M_ROOM_CREATE = "m.room.create"
    M_ROOM_POWER_LEVELS = "m.room.power_levels"
    M_ROOM_REDACTION = "m.room.redaction"


def addon(arg: Namespace, yaml: YAML) -> int:
    """Get Events from the Server.

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
    # get_event_ids(arg, yaml)
    # return 0

    address = (
        yaml.get("server", "ssh", "address")
        if yaml.get("server", "ssh", "address")
        else f"matrix.{yaml.get('server', 'api', 'domain')}"
    )

    # Todo better matching
    is_valid_sender: Match[str] | None = re.match(r"^\@.*\:.*\..*$", arg.user)
    is_valid_room_id = (
        re.match(r"^\!.*\:.*\..*$", arg.room_id) if arg.room_id else None
    )
    # try/except
    message_type: MessageType | None = None  # unset: AttributeError
    with suppress(AttributeError):
        try:
            message_type = MessageType[arg.type.replace(".", "_").upper()]
        except KeyError:  # message type is not in enum
            logger.error("Message type is not allowed or wrong.")
    if not is_valid_sender:
        logger.error(
            "The given user has an invalid format. Please make sure you "
            "use one with the correct format. "
            "Example: @username:domain.tld"
        )
        sys.exit(1)
    if not is_valid_room_id and is_valid_room_id is not None:
        logger.error(
            "The given room_id has an invalid format. Please make sure you "
            "use one with the correct format. "
            "Example: !iuyQXswfjgxQMZGrfQ:matrix.org"
        )
        sys.exit(1)

    room_id_str: str = (
        f" AND room_id = '{arg.room_id}'" if is_valid_room_id else ""
    )
    message_type_str: str = (
        f" AND type = '{message_type.value}'" if message_type else ""
    )
    query: str = (
        "SELECT json FROM event_json WHERE event_id IN ("
        "SELECT event_id FROM events WHERE sender = "
        f"'{arg.user}'"
        f"{room_id_str}"
        f"{message_type_str})"
    )
    cmd: str = "/usr/local/bin/matrix-postgres-cli -P pager"
    table: str = "synapse"

    command: str = f'sudo {cmd} -d {table} -c "{query}"'

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
            json_lst = ",".join(response.stdout[start:stop].split("\n"))
            logger.debug(f"{json_lst=}")

            try:
                print(json.dumps(json.loads(f"[{json_lst}]"), indent=4))
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
