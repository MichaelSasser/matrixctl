# matrixctl
# Copyright (c) 2020-2023  Michael Sasser <Michael@MichaelSasser.org>
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
import typing as t

from argparse import Namespace

from matrixctl.handlers.db import db_connect
from matrixctl.handlers.yaml import YAML
from matrixctl.sanitizers import MessageType
from matrixctl.sanitizers import sanitize_message_type
from matrixctl.sanitizers import sanitize_room_identifier
from matrixctl.sanitizers import sanitize_user_identifier


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


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
    # Sanitize user identifier
    user_identifier: str | t.Literal[False] | None = sanitize_user_identifier(
        arg.user,
    )
    if not user_identifier:
        return 1

    # Sanitize room identifier
    room_identifier: str | t.Literal[False] | None = sanitize_room_identifier(
        arg.room_id,
    )
    if room_identifier is False:
        return 1

    # Sanitize message_type
    message_type: MessageType | t.Literal[False] | None = (
        sanitize_message_type(arg.type)
    )
    if message_type is False:
        return 1

    query: str = (
        "SELECT json FROM event_json WHERE event_id IN ("
        "SELECT event_id FROM events WHERE sender = (%s)"
    )
    values = [user_identifier]

    # Add room identifier to the query
    if room_identifier:
        query += " AND room_id = (%s)"
        values.append(room_identifier)

    # Add message type to the query
    if message_type:
        values.append(message_type.value)
        query += " AND type = (%s)"

    query += ")"

    with db_connect(yaml) as conn, conn.cursor() as cur:
        cur.execute(query, values)
        try:
            print("[", end="")
            not_first_line: bool = False
            for event in cur:
                if not_first_line:
                    print(",")
                else:
                    not_first_line = True
                print(
                    json.dumps(json.loads(event[0]), indent=4),
                    end="",
                )
            print("]")
        except json.decoder.JSONDecodeError:
            logger.exception(
                "Unable to process the response data to JSON.",
            )
            return 1
    return 0


# vim: set ft=python :
