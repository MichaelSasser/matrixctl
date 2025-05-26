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

"""Use this module to add the ``serve-notice`` subcommand to ``matrixctl``."""

from __future__ import annotations

import typing as t

from argparse import ArgumentParser
from argparse import BooleanOptionalAction
from argparse import _SubParsersAction

from matrixctl.command import SubCommand
from matrixctl.command import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser(SubCommand.ROOM)
def subparser_send_event(
    subparsers: _SubParsersAction[t.Any],
    common_parser: ArgumentParser,
) -> None:
    """Create a subparser for the ``matrixctl server-notice`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction of typing.Any
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "send-event",
        help="Send an event to a room",
        parents=[common_parser],
    )
    parser.add_argument(
        "room",
        help=("The room identifier or alias"),
    )

    parser.add_argument(
        "content",
        help=("The Content as JSON string"),
    )
    parser.add_argument(
        "-t",
        "--type",
        help=("The type of the event to send (default: m.room.message)"),
        default="m.room.message",
    )
    parser.add_argument(
        "-s",
        "--state-key",
        help=("The state key of the event to send (only for state events"),
    )
    parser.add_argument(
        "--confirm",
        help=("Send the event without confirmation"),
        type=bool,
        default=True,
        action=BooleanOptionalAction,
    )
    parser.add_argument(
        "--force",
        help=("Ignore all warnings and send the event anyway"),
        type=bool,
    )
    parser.set_defaults(addon="send_event")


# vim: set ft=python :
