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
from matrixctl.print_helpers import human_readable_bool
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def to_table(
    users_list: list[JsonDict],
    len_domain: int,
) -> Generator[str, None, None]:
    """Use this function as helper to pint the users table.

    Examples
    --------
    .. code-block:: console

       $ matrixctl users
       +---------+-------------+---------------+-------+-------+--------------+
       | Name    | Deactivated | Shadow-Banned | Admin | Guest | Display Name |
       |---------+-------------+---------------+-------+-------|--------------+
       | dwight  | No          | No            | Yes   | No    | Dwight       |
       | pam     | No          | No            | No    | No    | Pam          |
       | jim     | No          | No            | No    | No    | Jim          |
       | creed   | No          | Yes           | No    | No    | Creed        |
       | stanley | No          | No            | No    | No    | Stanley      |
       | kevin   | No          | No            | No    | No    | Cookie       |
       | angela  | No          | No            | No    | No    | Angela       |
       | phyllis | No          | No            | No    | No    | Phyllis      |
       | tobi    | No          | No            | No    | No    | TobiHR       |
       | michael | No          | No            | Yes   | No    | Best Boss    |
       | andy    | No          | No            | No    | No    | Andy         |
       +---------+-------------+---------------+-------+-------+--------------+

    Parameters
    ----------
    users_list : list of matrixctl.typehints.JsonDict
        A list of rooms from the API.
    len_domain : int
        The length of the homeservers domain.

    Yields
    ------
    table_lines : str
        The table lines.

    """

    user_list: list[tuple[str, str, str, str, str, str]] = []

    for user in users_list:
        name = user["name"][1:-len_domain]
        deactivated: str = human_readable_bool(user["deactivated"])
        shadow_banned: str = human_readable_bool(user["shadow_banned"])
        admin: str = human_readable_bool(user["admin"])
        guest: str = human_readable_bool(user["is_guest"])
        display_name = user["displayname"]

        user_list.append(
            (
                name,
                deactivated,
                shadow_banned,
                admin,
                guest,
                display_name,
            ),
        )
    return table(
        user_list,
        (
            "Name",
            "Deactivated",
            "Shadow-Banned",
            "Admin",
            "Guest",
            "Display Name",
        ),
        sep=False,
    )


# vim: set ft=python :
