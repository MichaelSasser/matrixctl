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

"""Use this module to add the ``rooms`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from collections.abc import Generator

from matrixctl.handlers.table import table
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def to_table(rooms_list: list[JsonDict]) -> Generator[str, None, None]:
    """Use this function as helper to pint the room table.

    Parameters
    ----------
    rooms_list : list of matrixctl.typehints.JsonDict
        A list of rooms from the API.

    Yields
    ------
    table_lines : str
        The table lines.

    """

    room_list: list[tuple[str, str, str, str]] = []

    for room in rooms_list:
        name = room["name"]
        members: str = str(room["joined_members"])
        alias: str = room["canonical_alias"]
        room_id: str = room["room_id"]

        room_list.append(
            (
                name,
                members,
                alias,
                room_id,
            ),
        )
    return table(room_list, ("Name", "Members", "Alias", "Room ID"), sep=False)


# vim: set ft=python :
