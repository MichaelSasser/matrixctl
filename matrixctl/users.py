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
from __future__ import annotations

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction
from logging import fatal
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


def subparser_users(subparsers: SubParsersAction) -> None:
    parser: ArgumentParser = subparsers.add_parser("users", help="Lists users")
    parser.add_argument(
        "-g", "--guests", action="store_true", help="Shows the users"
    )
    parser.add_argument(
        "-b", "--no-bots", action="store_true", help="Hide bots"
    )
    parser.set_defaults(func=users)


def users(arg: Namespace) -> int:
    """Print a table of the matrix users.

    This function generates and prints a table of matrix user accounts.
    The table can be modified with:

    - the ``--guests`` switch: ``args.guests`` is True, else ``False``
    - the ``--no-bots`` switch: ``args.no_bots`` is True, else ``False``

    If you don't want any bots in the table use the ``--no-bots`` switch.
    If you want guests in the table use the ``--guests`` switch.

    **Example**

    .. code-block:: console

       $ matrixctl users --no-bots
       +----------------+---------------+------------+------------+
       | Name           | Deactivated   | Is Admin   | Is Guest   |
       |----------------+---------------+------------+------------|
       | dunder_mifflin | False         | True       | False      |
       | dwight         | False         | True       | False      |
       | pam            | False         | False      | False      |
       | jim            | False         | False      | False      |
       | creed          | False         | False      | False      |
       | stanley        | False         | False      | False      |
       | kevin          | False         | False      | False      |
       | angela         | False         | False      | False      |
       | phyllis        | False         | False      | False      |
       | tobi           | False         | False      | False      |
       | michael        | False         | True       | False      |
       | andy           | False         | False      | False      |
       +----------------+---------------+------------+------------+

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :return:          None
    """
    with TOML() as toml:
        len_domain = len(toml.get(("API", "Domain"))) + 1  # 1 for :
        from_user: int = 0
        users_list: List[JsonDict] = []

        # ToDo: API bool
        with API(
            toml.get(("API", "Domain")), toml.get(("API", "Token"))
        ) as api:
            api.url.path = "users"
            api.params = {"guests": "true" if arg.guests else "false"}

            while True:

                api.params = {"from": from_user}  # from must be in the loop
                try:
                    lst: JsonDict = api.request().json()
                except InternalResponseError:
                    fatal("Could not get the user table.")

                    return 1

                users_list += lst["users"]
                try:
                    from_user = lst["next_token"]
                except KeyError:
                    break

            user_list: List[Tuple[str, str, str, str]] = []

            for user in users_list:
                name = user["name"][1:-len_domain]
                no_passwd_hash: bool = user["password_hash"] == ""
                deactivated: str = human_readable_bool(user["deactivated"])
                admin: str = human_readable_bool(user["admin"])
                guest: str = human_readable_bool(user["is_guest"])

                # if no_bots and any([name.startswith(bot) for bot in BOTS]):
                #     continue

                if arg.no_bots and no_passwd_hash:
                    continue

                user_list.append((name, deactivated, admin, guest,))
            print(
                tabulate(
                    user_list,
                    headers=("Name", "Deactivated", "Is Admin", "Is Guest"),
                    tablefmt="psql",
                )
            )

    return 0


# vim: set ft=python :
