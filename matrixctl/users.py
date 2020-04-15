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
from argparse import Namespace
from tabulate import tabulate
from .config_handler import Config
from .api_handler import Api
from .typing import JsonDict

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_users(subparsers):
    users_parser = subparsers.add_parser("users", help="Lists users")
    users_parser.add_argument(
        "-g", "--guests", action="store_true", help="Shows the users"
    )
    users_parser.add_argument(
        "-b", "--no-bots", action="store_true", help="Hide bots"
    )
    users_parser.set_defaults(func=users)


def users(arg: Namespace, cfg: Config) -> None:
    """This function generates and prints a table of matrix user accounts.
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
    :param cfg:       The ``Config`` class
    :return:          None
    """

    with Api(cfg.api_domain, cfg.api_token) as api:
        len_domain = len(cfg.api_domain) + 1  # 1 for :
        from_user: int = 0
        users_list: list = []

        while True:
            lst: JsonDict = api.users(from_user, show_guests=arg.guests)

            users_list += lst["users"]
            try:
                from_user = lst["next_token"]
            except KeyError:
                break

        user_list: list = []

        for user in users_list:
            name = user["name"][1:-len_domain]
            no_passwd_hash: bool = user["password_hash"] == ""
            deactivated: bool = bool(int(user["deactivated"]))
            admin: bool = bool(int(user["admin"]))
            guest: bool = bool(int(user["is_guest"]))

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


# vim: set ft=python :
