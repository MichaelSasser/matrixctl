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

"""Use this module to add the ``users`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction
from typing import List
from typing import Tuple

from tabulate import tabulate

from .errors import InternalResponseError
from .handlers.api import API
from .handlers.toml import TOML
from .print_helpers import human_readable_bool
from .typing import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def subparser_users(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl users`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser("users", help="Lists users")
    parser.add_argument(
        "-a", "--all", action="store_true", help="Shows all users"
    )
    parser.add_argument(
        "-g", "--with-guests", action="store_true", help="Shows guests"
    )
    parser.add_argument(
        "-d",
        "--with-deactivated",
        action="store_true",
        help="Shows deactivated accounts",
    )
    parser.set_defaults(func=users)


def users(arg: Namespace) -> int:
    """Print a table of the matrix users.

    This function generates and prints a table of matrix user accounts.
    The table can be modified.

    - If you want guests in the table use the ``--with-guests`` switch.
    - If you want deactivated user in the table use the ``--with-deactivated``
      switch.


    Notes
    -----
    - Needs API version 2 (``synapse`` 1.28 or greater) to work.
    - API version 1 is deprecated. If you encounter problems please upgrade
      to the latest ``synapse`` release.

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
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    toml: TOML = TOML()
    len_domain = len(toml.get("API", "Domain")) + 1  # 1 for :
    from_user: int = 0
    users_list: List[JsonDict] = []

    # ToDo: API bool
    api: API = API(toml.get("API", "Domain"), toml.get("API", "Token"))
    api.url.api_version = "v2"
    api.url.path = "users"
    api.params = {"guests": "true" if arg.with_guests or arg.all else "false"}
    api.params = {
        "deactivated": "true" if arg.with_deactivated or arg.all else "false"
    }

    while True:

        api.params = {"from": from_user}  # from must be in the loop
        try:
            lst: JsonDict = api.request().json()
        except InternalResponseError:
            logger.critical("Could not get the user table.")

            return 1

        users_list += lst["users"]

        try:
            from_user = lst["next_token"]
        except KeyError:
            break

    user_list: List[Tuple[str, str, str, str, str, str]] = []

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
            )
        )
    print(
        tabulate(
            user_list,
            headers=(
                "Name",
                "Deactivated",
                "Shadow-Banned",
                "Admin",
                "Guest",
                "Display Name",
            ),
            tablefmt="psql",
        )
    )

    return 0


# vim: set ft=python :
