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

import datetime
import json
import logging
import typing as t

from argparse import Namespace
from sys import stdout

from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.text import Text
from rich.theme import Theme

from .parser import OutputType

from matrixctl.handlers.api import download_media_to_buf
from matrixctl.handlers.db import db_connect
from matrixctl.handlers.yaml import YAML
from matrixctl.print_helpers import imgcat
from matrixctl.sanitizers import MessageType
from matrixctl.sanitizers import sanitize_message_type
from matrixctl.sanitizers import sanitize_room_identifier
from matrixctl.sanitizers import sanitize_user_identifier
from matrixctl.handlers.rows import Ctx, to_row_context


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


class HighlighterMatrixUser(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "example."
    highlights = [r"(?P<matrix_user>@[\w-]+:([\w-]+\.)+[\w-]+)"]


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
        sanitize_message_type(arg.event_type)
    )
    if message_type is False:
        return 1

    query: str = "WITH evs AS (SELECT event_id, origin_server_ts, received_ts FROM events WHERE sender = (%s)"
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

    query += "SELECT event_json.event_id, event_json.json, evs.origin_server_ts, evs.received_ts FROM event_json INNER JOIN evs ON event_json.event_id = evs.event_id ORDER BY evs.origin_server_ts ASC"

    with db_connect(yaml) as conn, conn.cursor() as cur:
        cur.execute(query, values)
        if arg.output_format == OutputType.ROWS:
            try:
                for event in cur:
                    event_id = event[0]
                    ev = json.loads(event[1])

                    origin_server_ts_ = int(event[2])
                    received_ts_ = int(event[3])

                    origin_server_ts = datetime.datetime.fromtimestamp(
                        origin_server_ts_ / 1000.0, tz=datetime.timezone.utc
                    )
                    received_ts = datetime.datetime.fromtimestamp(
                        received_ts_ / 1000.0, tz=datetime.timezone.utc
                    )

                    tdelta: datetime.timedelta = received_ts.replace(
                        microsecond=0
                    ) - origin_server_ts.replace(microsecond=0)

                    ts_str = (
                        origin_server_ts.replace(microsecond=0)
                        .isoformat()
                        .replace("+00:00", "")
                    )
                    room_id = ev.get("room_id")

                    sender = ev.get("sender")

                    kind_: str = ev.get("type")
                    kind: MessageType | str
                    try:
                        kind = MessageType.from_string(kind_)
                    except ValueError:
                        kind = kind_

                    ctx: Ctx = to_row_context(ev, yaml)

                    theme = Theme({"example.matrix_user": "magenta bold"})
                    console = Console(
                        highlighter=HighlighterMatrixUser(), theme=theme
                    )
                    text = Text()
                    text.append(ts_str, style="blue bold")
                    text.append(" | ", style="bright_black")
                    text.append(room_id, style="bright_yellow")
                    text.append(" | ", style="bright_black")
                    text.append(sender, style="bright_magenta")
                    text.append(" | ", style="bright_black")
                    text.append(kind_, style="steel_blue1")
                    text.append(" | ", style="bright_black")
                    text.append(event_id, style="purple3")
                    text.append(" | ", style="bright_black")
                    text.append_text(ctx.text)
                    if tdelta.total_seconds() > 30.0:
                        text.append(" | ", style="bright_black")
                        text.append(f"Δt = {tdelta}", style="red bold")
                    console.print(
                        text,
                        soft_wrap=True,
                        highlight=True,
                    )
                    if len(ctx.post_buf) > 0:
                        stdout.buffer.write(ctx.post_buf)
                        stdout.flush()

                    print()

            except json.decoder.JSONDecodeError:
                logger.exception(
                    "Unable to process the response data to JSON.",
                )
                return 1
        if arg.output_format == OutputType.JSON:
            try:
                print("[", end="")
                not_first_line: bool = False
                for event in cur:
                    if not_first_line:
                        print(",")
                    else:
                        not_first_line = True
                    print(
                        json.dumps(json.loads(event[1]), indent=4),
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
