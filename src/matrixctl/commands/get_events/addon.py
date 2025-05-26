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
from copy import deepcopy
from enum import Enum
from sys import stdout

from psycopg.cursor import Cursor
from psycopg.rows import TupleRow
from rich.console import Console
from rich.text import Text

from .parser import OutputType

from matrixctl.handlers.db import db_connect
from matrixctl.handlers.rows import Ctx
from matrixctl.handlers.rows import to_row_context
from matrixctl.handlers.yaml import YAML
from matrixctl.sanitizers import EventType
from matrixctl.sanitizers import sanitize_event_type
from matrixctl.sanitizers import sanitize_room_identifier
from matrixctl.sanitizers import sanitize_sequence
from matrixctl.sanitizers import sanitize_user_identifier


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)

WARN_FOR_EVENTS_OLDER_THAN: float = 30.0


def add_tuple_to_query_workaround(
    query: str,
    values: list[str | int | tuple[str | int, ...]],
    args: tuple[str | Enum, ...] | t.Literal[False] | None,
    token: str | Enum,
) -> tuple[str, list[str | int | tuple[str | int, ...]]]:
    """Use this function as a workaround for adding a tuple to the query."""
    query_: str = deepcopy(query)
    values_: list[str | int | tuple[str | int, ...]] = deepcopy(values)
    if args:  # One element
        if len(args) == 1:
            query_ += f" AND {token} = (%s)"
            if isinstance(args[0], Enum):
                values_.append(args[0].value)
            else:
                values_.append(args[0])
        else:  # Multiple elements
            # TODO: `foo = ANY(%s)` does not seem work. Something not getting
            #       escaped properly?
            query_ += f" AND {token} IN ("
            for i, arg in enumerate(args):
                if i > 0:
                    query_ += ", "
                query_ += "(%s)"
                if isinstance(arg, Enum):
                    values_.append(arg.value)
                else:
                    values_.append(arg)
            query_ += ")"
    return query_, values_


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

    # Sanitize the input
    user_identifiers: tuple[str, ...] | t.Literal[False] | None = (
        sanitize_sequence(sanitize_user_identifier, arg.users)
    )
    room_identifiers: tuple[str, ...] | t.Literal[False] | None = (
        sanitize_sequence(
            sanitize_room_identifier,
            arg.room_ids,
            yaml.get_room_alias,
        )
    )
    event_types: tuple[EventType, ...] | t.Literal[False] | None = (
        sanitize_sequence(sanitize_event_type, arg.event_types)
    )
    if any(
        b is False for b in {user_identifiers, room_identifiers, event_types}
    ):
        return 1  # sanitation failed

    since: datetime.datetime = arg.since or datetime.datetime(
        1970, 1, 1, tzinfo=datetime.timezone.utc
    )
    until: datetime.datetime | None = arg.until

    query: str = (
        "WITH evs AS ("
        "SELECT event_id, origin_server_ts, received_ts "
        "FROM events WHERE origin_server_ts >= (%s)"
    )
    values: list[str | int | tuple[str | int, ...]] = [
        int(since.timestamp() * 1000)
    ]

    # Add until to the query
    if until:
        query += " AND origin_server_ts < (%s)"
        values.append(int(until.timestamp() * 1000))

    # Add user identifier to the query
    query, values = add_tuple_to_query_workaround(
        query, values, user_identifiers, "sender"
    )

    # Add room identifier to the query
    query, values = add_tuple_to_query_workaround(
        query, values, room_identifiers, "room_id"
    )

    # Add message type to the query
    query, values = add_tuple_to_query_workaround(
        query, values, event_types, "type"
    )

    query += ") "

    query += (
        "SELECT "
        "event_json.event_id, "
        "event_json.json, "
        "evs.origin_server_ts, "
        "evs.received_ts "
        "FROM "
        "event_json INNER JOIN evs ON event_json.event_id = evs.event_id "
        "ORDER BY evs.origin_server_ts ASC"
    )

    with db_connect(yaml) as conn, conn.cursor() as cur:
        cur.execute(query, tuple(values))
        if arg.output_format == OutputType.ROWS:
            return output_as_rows(cur, yaml)
        if arg.output_format == OutputType.JSON:
            return output_as_json(cur)
    return 0


def output_as_rows(cur: Cursor[TupleRow], yaml: YAML) -> int:
    """Output the events as rows."""
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

            kind: str = ev.get("type")

            ctx: Ctx = to_row_context(ev, yaml)

            console = Console()
            text = Text()
            text.append(ts_str, style="blue bold")
            text.append(" | ", style="bright_black")
            text.append(room_id, style="bright_yellow")
            text.append(" | ", style="bright_black")
            text.append(sender, style="bright_magenta")
            text.append(" | ", style="bright_black")
            text.append(kind, style="steel_blue1")
            text.append(" | ", style="bright_black")
            text.append(event_id, style="purple3")
            text.append(" | ", style="bright_black")
            text.append_text(ctx.text)
            if tdelta.total_seconds() > WARN_FOR_EVENTS_OLDER_THAN:
                text.append(" | ", style="bright_black")
                text.append(f"Δt = {tdelta}", style="red bold")
            console.print(
                text,
                soft_wrap=True,
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
    return 0


def output_as_json(cur: Cursor[TupleRow]) -> int:
    """Output the events as JSON."""
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
