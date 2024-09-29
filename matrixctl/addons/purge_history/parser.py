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

"""The purge-history command allows to purge historic events from the database.

Use this module to add the ``purge-histoy`` subcommand to ``matrixctl``.
"""

from __future__ import annotations

import typing as t

from argparse import ArgumentParser
from argparse import _SubParsersAction

from matrixctl.addon_manager import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser
def subparser_purge_history(subparsers: _SubParsersAction[t.Any]) -> None:
    """Create a subparser for the ``matrixctl purge-history`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction of typing.Any
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "purge-history",
        help="Purge historic events from the database",
    )
    parser.add_argument(
        "-l",
        "--local-events",
        action="store_true",
        help="Delete local message events as well",
    )
    parser.add_argument(
        "room_id",
        type=str,
        help="The Room to purge historic message events in",
    )
    parser.add_argument(
        "event_or_timestamp",
        type=str,
        nargs="?",
        default=None,
        help=(
            "An event identifier or timestamp (UNIX epoch) as point in time,"
            "to which events will be purged"
        ),
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="No questions asked",
    )
    parser.set_defaults(addon="purge_history")


# vim: set ft=python :
