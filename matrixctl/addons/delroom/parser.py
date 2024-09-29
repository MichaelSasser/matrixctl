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

"""Use this module to add the ``delroom`` subcommand to ``matrixctl``."""

from __future__ import annotations

import typing as t

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import _SubParsersAction

from matrixctl.addon_manager import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser
def subparser_delroom(subparsers: _SubParsersAction[t.Any]) -> None:
    """Create a subparser for the ``matrixctl delroom`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction of typing.Any
        The object which is returned by
        ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "delroom",
        help="Shutdown a room",
        formatter_class=RawDescriptionHelpFormatter,
        description=(
            "This command uses the Delete Room API, which removes rooms from"
            " the server.\n\nOptional:\nBy default: All data of the old room"
            " will be purged from the database.\nOptional: Access for local"
            " users to join the room ever again, can be blocked\nOptional: A"
            " new room can be created with a new room administrator. When a"
            " new room is created, all local users will be invited. They will"
            " have power level -10, which means, they are muted by default."
            " With the message argument a message can be sent to the new room."
            " All room aliases will be transfared to the new room."
        ),
    )
    parser.add_argument("room", type=str, help="The room identifier")
    parser.add_argument(
        "new_room_admin",
        type=str,
        nargs="?",
        default=None,
        help=(
            "Move all local users and room aliases automatically to a new "
            "room, where this user will become the new room admin. "
            "Users invited to the new room will have power level -10"
        ),
    )
    parser.add_argument(
        "new_room_name",
        type=str,
        nargs="?",
        default="Content Violation Notification",
        help=(
            "The name of the new room. default: "
            '"Content Violation Notification"'
        ),
    )
    parser.add_argument(
        "message",
        type=str,
        nargs="?",
        default=None,
        help=(
            "The message sent to the new room. default: "
            '"<old room identifier> has been shutdown due to content '
            'violations on this server. Please review our Terms of Service."'
        ),
    )
    parser.add_argument(
        "-b",
        "--block",
        action="store_true",
        help="Prevents any new joins to the old room",
    )
    parser.add_argument(
        "--no-purge",
        action="store_false",
        help=(
            "Do not remove all trace of the old room from the database after "
            "removing all local users"
        ),
    )
    parser.add_argument(
        "--force-purge",
        action="store_true",
        help=(
            "force a purge to go ahead even if there are local users still in "
            "the room. Do not use this unless a regular purge operation fails"
        ),
    )
    parser.set_defaults(addon="delroom")


# vim: set ft=python :
