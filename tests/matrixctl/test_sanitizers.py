# matrixctl
# Copyright (c) 2021-2023  Michael Sasser <Michael@MichaelSasser.org>
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

"""Test the sanitizers."""

from __future__ import annotations

import typing as t

from matrixctl import sanitizers


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

###############################################################################
#                            message_type
###############################################################################


def test_sanitize_message_type_m_room_message_1() -> None:
    """Test valid message type as MessageType."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_MESSAGE

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_message_2() -> None:
    """Test valid message type as string."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_MESSAGE
    testdata: str = "M.ROOM.MESSAGE"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_name_1() -> None:
    """Test valid message type as MessageType."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_MESSAGE

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_name_2() -> None:
    """Test valid message type as string."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_NAME
    testdata: str = "M.ROOM.NAME"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_topic_1() -> None:
    """Test valid message type as MessageType."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_TOPIC

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_topic_2() -> None:
    """Test valid message type as string."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_TOPIC
    testdata: str = "M.ROOM.TOPIC"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_avatar_1() -> None:
    """Test valid message type as MessageType."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_AVATAR

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_avatar_2() -> None:
    """Test valid message type as string."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_AVATAR
    testdata: str = "M.ROOM.AVATAR"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_pinned_events_1() -> None:
    """Test valid message type as MessageType."""

    # Setup
    desired: sanitizers.MessageType = (
        sanitizers.MessageType.M_ROOM_PINNED_EVENTS
    )

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_pinned_events_2() -> None:
    """Test valid message type as string."""

    # Setup
    desired: sanitizers.MessageType = (
        sanitizers.MessageType.M_ROOM_PINNED_EVENTS
    )
    testdata: str = "M.ROOM.PINNED_EVENTS"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_member_1() -> None:
    """Test valid message type as MessageType."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_MEMBER

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_member_2() -> None:
    """Test valid message type as string."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_MEMBER
    testdata: str = "M.ROOM.MEMBER"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_join_rules_1() -> None:
    """Test valid message type as MessageType."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_JOIN_RULES

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_join_rules_2() -> None:
    """Test valid message type as string."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_JOIN_RULES
    testdata: str = "M.ROOM.JOIN_RULES"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_create_1() -> None:
    """Test valid message type as MessageType."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_CREATE

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_create_2() -> None:
    """Test valid message type as string."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_CREATE
    testdata: str = "M.ROOM.CREATE"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_power_levels_1() -> None:
    """Test valid message type as MessageType."""

    # Setup
    desired: sanitizers.MessageType = (
        sanitizers.MessageType.M_ROOM_POWER_LEVELS
    )

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_power_levels_2() -> None:
    """Test valid message type as string."""

    # Setup
    desired: sanitizers.MessageType = (
        sanitizers.MessageType.M_ROOM_POWER_LEVELS
    )
    testdata: str = "M.ROOM.POWER_LEVELS"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_redaction_1() -> None:
    """Test valid message type as MessageType."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_REDACTION

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_m_room_redaction_2() -> None:
    """Test valid message type as string."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_REDACTION
    testdata: str = "M.ROOM.REDACTION"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_invalid() -> None:
    """Test invalid message type as string."""

    # Setup
    desired: t.Literal[False] = False
    testdata: str = "M.ROOM.INVALID_TYPE"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_with_spaces() -> None:
    """Test valid message type as string with spaces around."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_REDACTION
    testdata: str = " M.ROOM.REDACTION "

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_lower_case() -> None:
    """Test valid message type as lowercase string."""

    # Setup
    desired: sanitizers.MessageType = sanitizers.MessageType.M_ROOM_REDACTION
    testdata: str = "m.room.redaction"

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_message_type_none() -> None:
    """Test none case."""

    # Setup
    desired: None = None
    testdata: None = None

    # Exercise
    actual: sanitizers.MessageType | t.Literal[False] | None = (
        sanitizers.sanitize_message_type(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


###############################################################################
#                         event_identifier
###############################################################################


def test_sanitize_event_identifier_1() -> None:
    """Test valid identifier."""

    # Setup
    desired: str = "$event-abcdefghijklmH4omLrEumu7Pd01Qp-LySpK_Y"

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_event_identifier(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_event_identifier_2() -> None:
    """Test valid identifier with spaces around."""

    # Setup
    desired: str = "$event-abcdefghijklmH4omLrEumu7Pd01Qp-LySpK_Y"
    testdata: str = " $event-abcdefghijklmH4omLrEumu7Pd01Qp-LySpK_Y "

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_event_identifier(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_event_identifier_3() -> None:
    """Test invalid identifier (without $)."""

    # Setup
    desired: bool = False
    testdata: str = "event-abcdefghijklmH4omLrEumu7Pd01Qp-LySpK_Y"

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_event_identifier(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_event_identifier_4() -> None:
    """Test invalid identifier (empty str)."""

    # Setup
    desired: bool = False
    testdata: str = ""

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_event_identifier(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_event_identifier_5() -> None:
    """Test missing identifier (None)."""

    # Setup
    desired: None = None
    testdata: None = None

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_event_identifier(testdata)
    )

    # Verify
    assert actual == desired
    # Cleanup - None


def test_sanitize_event_identifier_6() -> None:
    """Test wrong type."""

    # Setup
    desired: t.Literal[False] = False
    testdata: set[str] = {"hello"}

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_event_identifier(testdata)
    )

    # Verify
    assert actual == desired
    # Cleanup - None


###############################################################################
#                         user_identifier
###############################################################################


def test_sanitize_user_identifier_1() -> None:
    """Test valid identifier."""

    # Setup
    desired: str = "@user:domain.tld"

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_user_identifier(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_user_identifier_2() -> None:
    """Test valid identifier with spaces around."""

    # Setup
    desired: str = "@user:domain.tld"
    testdata: str = " @user:domain.tld "

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_user_identifier(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_user_identifier_3() -> None:
    """Test invalid identifier (without $)."""

    # Setup
    desired: bool = False
    testdata: str = " user:domain.tld "

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_user_identifier(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_user_identifier_4() -> None:
    """Test invalid identifier (empty str)."""

    # Setup
    desired: bool = False
    testdata: str = ""

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_user_identifier(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_user_identifier_5() -> None:
    """Test missing identifier (None)."""

    # Setup
    desired: None = None
    testdata: None = None

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_user_identifier(testdata)
    )

    # Verify
    assert actual == desired
    # Cleanup - None


def test_sanitize_user_identifier_6() -> None:
    """Test wrong type."""

    # Setup
    desired: t.Literal[False] = False
    testdata: set[str] = {"hello"}

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_user_identifier(testdata)
    )

    # Verify
    assert actual == desired
    # Cleanup - None


###############################################################################
#                         room_identifier
###############################################################################


def test_sanitize_room_identifier_1() -> None:
    """Test valid identifier."""

    # Setup
    desired: str = "!room:domain.tld"

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_room_identifier(desired)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_room_identifier_2() -> None:
    """Test valid identifier with spaces around."""

    # Setup
    desired: str = "!room:domain.tld"
    testdata: str = " !room:domain.tld "

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_room_identifier(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_room_identifier_3() -> None:
    """Test invalid identifier (without $)."""

    # Setup
    desired: bool = False
    testdata: str = "room:domain.tld"

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_room_identifier(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_room_identifier_4() -> None:
    """Test invalid identifier (empty str)."""

    # Setup
    desired: bool = False
    testdata: str = ""

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_room_identifier(testdata)
    )

    # Verify
    assert actual == desired

    # Cleanup - None


def test_sanitize_room_identifier_5() -> None:
    """Test missing identifier (None)."""

    # Setup
    desired: None = None
    testdata: None = None

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_room_identifier(testdata)
    )

    # Verify
    assert actual == desired
    # Cleanup - None


def test_sanitize_room_identifier_6() -> None:
    """Test wrong type."""

    # Setup
    desired: t.Literal[False] = False
    testdata: set[str] = {"hello"}

    # Exercise
    actual: str | t.Literal[False] | None = (
        sanitizers.sanitize_room_identifier(testdata)
    )

    # Verify
    assert actual == desired
    # Cleanup - None


# vim: set ft=python :
