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


def format_bytes(size: int) -> str:
    """Format bytes (storage) into a string using the correct prefix.

    Parameters
    ----------
    size : int
        An integer representing some storage size in bytes

    Returns
    -------
    formatted : str
        The size formatted with a prefix of bytes.

    """
    fsize: float = float(size)
    power = 2**10
    n = 0
    prefix = {0: "", 1: "k", 2: "M", 3: "G", 4: "T"}
    while fsize > power:
        fsize /= power
        n += 1
    return f"{fsize:1.2f} {prefix[n]+'B'}"


def to_table(rooms_list: list[JsonDict]) -> Generator[str, None, None]:
    """Use this function as helper to pint the largest-room table.

    Parameters
    ----------
    rooms_list : list of matrixctl.typehints.JsonDict
        A list of rooms from the API.

    Yields
    ------
    table_lines : str
        The table lines.

    """

    room_list: list[tuple[str, str]] = []

    for room in rooms_list:
        room_id = room["room_id"]
        size: int = int(room["estimated_size"])

        room_list.append(
            (
                room_id,
                format_bytes(size),
            ),
        )
    return table(room_list, ("Room ID", "Estimated Size"), sep=False)


# vim: set ft=python :
