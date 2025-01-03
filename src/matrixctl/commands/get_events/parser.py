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
from matrixctl.argparse_action import ArgparseActionEnum


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
    parser.add_argument("user", help="The user (e.g. @foo:bar.baz)")
    parser.add_argument("room_id", nargs="?", help="The room identifier")
    parser.add_argument("-e", "--event-type", help="The event type")
    parser.add_argument(
        "-f",
        "--output-format",
        type=OutputType,
        action=ArgparseActionEnum,
        default=OutputType.JSON,
        help="The Output type (rows, json)",
    )
    parser.set_defaults(addon="get_events")


# vim: set ft=python :
