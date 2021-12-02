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

"""Use the functions of this module as printing helpers."""

from __future__ import annotations

import logging
import re
import typing as t

from contextlib import suppress
from enum import Enum
from enum import unique


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


EVENT_ID_PATTERN: t.Pattern[str] = re.compile(r"^\$[0-9a-zA-Z.=_-]{1,255}$")
USER_ID_PATTERN: t.Pattern[str] = re.compile(r"^\@.*\:.*\..*$")
ROOM_ID_PATTERN: t.Pattern[str] = re.compile(r"^\!.*\:.*\..*$")


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


def sanitize_message_type(
    message_type: str | MessageType,
) -> MessageType | t.Literal[False] | None:
    """Sanitize an message type.

    Parameters
    ----------
    message_type : typing.Any
        The event identifier to sanitize

    Returns
    -------
    message_type_sanitized : typing.Literal[False] or MessageType, optional
        The function returns ``None`` if ``message_type`` is ``None``,
        ``MessageType``, if it is valid, otherwise ``False``

    """
    if isinstance(message_type, MessageType) or message_type is None:
        return message_type
    with suppress(TypeError, KeyError, AttributeError):
        return MessageType[message_type.strip().replace(".", "_").upper()]
    logger.error("The message type is not wrong.")
    return False


def sanitize_event_identifier(
    event_identifier: t.Any,
) -> str | t.Literal[False] | None:
    """Sanitize an event identifier.

    Parameters
    ----------
    event_identifier : typeing.Any
        The event identifier to sanitize

    Returns
    -------
    result : typing.Literal[False] or str, optional
        The function returns ``None`` if ``event_identifier`` is ``None``,
        the sanitized string, when it is valid, otherwise ``False``

    """
    if event_identifier is None:
        return None
    with suppress(TypeError, AttributeError):
        event_identifier = str(event_identifier).strip()
        if EVENT_ID_PATTERN.match(event_identifier):
            return t.cast(str, event_identifier)
    logger.error(
        "The given event identifier has an invalid format. Please make"
        " sure you use one with the correct format. For example:"
        " $tjeDdqYAk9BDLAUcniGUy640e_D9TrWU2RmCksJQQEQ"
    )
    return False


def sanitize_user_identifier(
    user_identifier: t.Any,
) -> str | t.Literal[False] | None:
    """Sanitize an user identifier.

    Parameters
    ----------
    user_identifier : typing.Any
        The user identifier to sanitize

    Returns
    -------
    event_identifier_sanitized : typing.Literal[False] or str, optional
        The function returns ``None`` if ``user_identifier`` is ``None``,
        the sanitized string, when it is valid, otherwise ``False``

    """
    if user_identifier is None:
        return None
    with suppress(TypeError, AttributeError):
        user_identifier = str(user_identifier).strip()
        if USER_ID_PATTERN.match(user_identifier):
            return t.cast(str, user_identifier)
    logger.error(
        "The given user identifier has an invalid format. Please make sure"
        " you use one with the correct format. For example:"
        " @username:domain.tld"
    )
    return False


def sanitize_room_identifier(
    room_identifier: t.Any,
) -> str | t.Literal[False] | None:
    """Sanitize an room identifier.

    Parameters
    ----------
    room_identifier : typing.Any
        The room identifier to sanitize

    Returns
    -------
    room_identifier_sanitized : typing.Literal[False] or str, optional
        The function returns ``None`` if ``room_identifier`` is ``None``,
        the sanitized string, when it is valid, otherwise ``False``

    """
    if room_identifier is None:
        return None
    with suppress(TypeError, AttributeError):
        room_identifier = str(room_identifier).strip()
        if ROOM_ID_PATTERN.match(room_identifier):
            return t.cast(str, room_identifier)
    logger.error(
        "The given room identifier has an invalid format. Please make sure"
        " you use one with the correct format. For example:"
        " !iuyQXswfjgxQMZGrfQ:matrix.org"
    )
    return False


# vim: set ft=python :
