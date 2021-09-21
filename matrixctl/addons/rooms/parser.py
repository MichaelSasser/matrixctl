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

"""Use this module to add the ``rooms`` subcommand to ``matrixctl``."""

from __future__ import annotations

from argparse import ArgumentParser
from argparse import _SubParsersAction

from matrixctl.addon_manager import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser
def subparser_rooms(subparsers: _SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl rooms`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser("rooms", help="List rooms")
    parser.add_argument(
        "limit",
        type=int,
        default=-1,
        nargs="?",
        help="The number of users to show",
    )
    parser.add_argument(
        "-s",
        "--order-by-size",
        action="store_true",
        help="Order the rooms by size instead of alphabetical",
    )
    parser.add_argument(
        "-r", "--reverse", action="store_true", help="Reverse the order"
    )
    parser.add_argument(
        "filter",
        type=str,
        nargs="?",
        default=None,
        help="Search for rooms with a specific search term (Case-Sensitive)",
    )

    parser.add_argument(
        "-j", "--to-json", action="store_true", help="Output the data as JSON"
    )
    parser.set_defaults(addon="rooms")


# vim: set ft=python :
