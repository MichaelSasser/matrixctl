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

import logging

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction

from tabulate import tabulate

from .errors import InternalResponseError
from .handlers.api import RequestBuilder
from .handlers.api import request
from .handlers.toml import TOML
from .typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def subparser_rooms(subparsers: SubParsersAction) -> None:
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
        "-s",
        "--order-by-size",
        action="store_true",
        help="Order the rooms by size instead of alphabetical",
    )
    parser.add_argument(
        "-r", "--reverse", action="store_true", help="Reverse the order"
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=0,
        help="The number of rooms to show",
    )
    parser.add_argument(
        "filter",
        type=str,
        nargs="?",
        default=None,
        help="Search for rooms with a specific search term (Case-Sensitive)",
    )
    parser.set_defaults(func=rooms)


def rooms(arg: Namespace) -> int:
    """Generate a table of the matrix rooms.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    toml: TOML = TOML()
    from_room: int = 0
    rooms_list: list[JsonDict] = []

    req: RequestBuilder = RequestBuilder(
        token=toml.get("API", "Token"),
        domain=toml.get("API", "Domain"),
        path="rooms",
        api_version="v1",
    )

    if arg.number > 0:
        req.params["limit"] = arg.number

    if arg.filter:
        req.params["search_term"] = arg.filter

    if arg.reverse:
        req.params["dir"] = "b"

    if arg.order_by_size:
        req.params["order_by"] = "size"

    while True:

        req.params["from"] = from_room  # from must be in the loop
        try:
            lst: JsonDict = request(req).json()
        except InternalResponseError:
            logger.critical("Could not get the room table.")

            return 1

        rooms_list += lst["rooms"]
        try:
            from_room = lst["next_token"]
        except KeyError:
            break
    print_rooms_table(rooms_list)

    return 0


def print_rooms_table(rooms_list: list[JsonDict]) -> None:
    """Use this function as helper to pint the room table.

    Parameters
    ----------
    rooms_list : list of matrixctl.typehints.JsonDict
        A list of rooms from the API.

    Returns
    -------
    None

    """

    room_list: list[tuple[str, int, str, str]] = []

    for room in rooms_list:
        name = room["name"]
        members: int = room["joined_members"]
        alias: str = room["canonical_alias"]
        room_id: str = room["room_id"]

        room_list.append(
            (
                name,
                members,
                alias,
                room_id,
            )
        )
    print(
        tabulate(
            room_list,
            headers=("Name", "Members", "Alias", "Room ID"),
            tablefmt="psql",
        )
    )


# vim: set ft=python :
