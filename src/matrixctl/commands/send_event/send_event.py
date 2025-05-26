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

"""Use this module to send events to a room."""

from __future__ import annotations

import json
import logging
import typing as t

from rich import print_json
from rich.prompt import Confirm

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.sanitizers import EventType
from matrixctl.sanitizers import sanitize_event_type
from matrixctl.sanitizers import sanitize_room_identifier
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def send_event(  # noqa: PLR0913 C901 PLR0912 PLR0911
    yaml: YAML,
    room: str,
    type_: str,
    content: JsonDict,
    state_key: str | None = None,
    *,
    confirm: bool = True,
    force: bool = False,
) -> int:
    """Send an event to a room.

    Parameters
    ----------
    room : str
        The room identifier or alias.
    type : str
        The type of the event to send (default: m.room.message).
    content : JsonDict
        The content of the event.
    state_key : str | None, optional
        The state key of the event, by default None.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    # room identifier
    sanitized_room: str | t.Literal[False] | None = sanitize_room_identifier(
        room, yaml.get_room_alias
    )
    if sanitized_room is None:
        logger.error("Room identifier is missing")
        return 1
    if sanitized_room is False:  # Literal[False]
        if force:
            logger.warning(
                (
                    "The room identifier '%s' is not valid. "
                    "Due to the use of the force argument, this is being "
                    "ignored."
                ),
                room,
            )
            sanitized_room = room
        else:
            logger.error("The room identifier '%s' is not valid.", room)
            return 1

    # event type
    sanitized_event_type: str | EventType | t.Literal[False] | None = (
        sanitize_event_type(type_)
    )
    if sanitized_event_type is None:
        logger.error("event_type is missing")
        return 1
    if sanitized_event_type is False:  # Literal[False]
        if force:
            logger.warning(
                (
                    "The event type '%s' is not valid. "
                    "Due to the use of the force argument, this is being "
                    "ignored."
                ),
                type_,
            )
            sanitized_event_type = type_
        else:
            logger.error("The event type '%s' is not valid.", room)
            return 1
    if isinstance(sanitized_event_type, EventType):
        sanitized_event_type = sanitized_event_type.value

    ev: JsonDict = content

    if confirm:
        print(
            f"Sending event with type '{sanitized_event_type}' to "
            f"room '{sanitized_room}':"
        )
        print_json(json.dumps(ev))

        is_confirmed = Confirm.ask("Is this correct?")
        if not is_confirmed:
            return 2
    else:
        logger.debug(
            "Sending event with type '%s' to room '%s': %s",
            sanitized_event_type,
            sanitized_room,
            ev,
        )

    path: str
    if state_key:
        path = (
            f"/_matrix/client/v3/rooms/{sanitized_room}/state"
            f"/{sanitized_event_type}/{state_key}"
        )
    else:
        path = (
            f"/_matrix/client/v3/rooms/{sanitized_room}/send"
            f"/{sanitized_event_type}"
        )

    req: RequestBuilder = RequestBuilder(
        token=yaml.get_api_token(),
        domain=yaml.get("server", "api", "domain"),
        path=path,
        method="POST",
        json=ev,
    )

    try:
        resp = request(req)
        resp.raise_for_status()
    except InternalResponseError:
        logger.exception("Sending the event was unsuccessful.")
        return 1

    return 0


# vim: set ft=python :
