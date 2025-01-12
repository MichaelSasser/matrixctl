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

"""Use this module to get an events of an user from the Database."""

from __future__ import annotations

import typing as t

from argparse import ArgumentParser
from argparse import _SubParsersAction
from enum import Enum
from enum import unique

from matrixctl.addon_manager import subparser
from matrixctl.argparse_action import ArgparseActionDateParser
from matrixctl.argparse_action import ArgparseActionEnum
from matrixctl.argparse_action import TimeDirection


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@unique
class OutputType(Enum):
    """Use this enum for describing the possible output types.

    Supported output types are:

    =========== ===================================================
    Output Type Description
    =========== ===================================================
    rows        Output raw JSON.
    json        Output only a summary as row.
    =========== ===================================================

    """

    ROWS = "rows"
    JSON = "json"


@subparser
def subparser_get_events(subparsers: _SubParsersAction[t.Any]) -> None:
    """Create a subparser for the ``matrixctl get-event`` command.

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
        "get-events",
        help="Get events from the database",
    )
    parser.add_argument(
        "users",
        nargs="*",
        help="The users (e.g. @michael:foo.bar,@dwight:foo.bar)",
    )
    parser.add_argument(
        "-r", "--room_ids", nargs="+", help="The room identifiers"
    )
    parser.add_argument(
        "-e", "--event-types", nargs="+", help="The event types"
    )
    parser.add_argument(
        "-f",
        "--output-format",
        type=OutputType,
        action=ArgparseActionEnum,
        default=OutputType.ROWS,
        help="The Output type (default: 'rows')",
    )
    parser.add_argument(
        "-s",
        "--since",
        action=ArgparseActionDateParser,
        time_direction=TimeDirection.PAST,
        help=(
            "Show events on or newer than the specified date. "
            "(Date must be in the past)"
        ),
    )
    parser.add_argument(
        "-u",
        "--until",
        action=ArgparseActionDateParser,
        time_direction=TimeDirection.PAST,
        help=(
            "Show events on or older than the specified date. "
            "(Date must be in the past)"
        ),
    )
    parser.set_defaults(addon="get_events")


# vim: set ft=python :
