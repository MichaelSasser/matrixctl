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

import datetime
import sys

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction
from logging import debug
from logging import error
from logging import fatal
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from tabulate import tabulate

from .errors import InternalResponseError
from .handlers.api import API
from .handlers.toml import TOML
from .print_helpers import human_readable_bool
from .typing import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_user(subparsers: SubParsersAction) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "user", help="Get information about a specific user"
    )
    parser.add_argument("user", help="The username of the user")
    parser.set_defaults(func=user)


def make_human_readable(
    k: str, user_dict: Dict[str, str], len_domain: int
) -> Tuple[str, str]:

    key: Optional[str] = None
    value: Union[str]

    if k == "name":
        value = str(user_dict[k][1:-len_domain])
    elif k == "is_guest":
        value = human_readable_bool(user_dict[k])
        key = "Guest"
    elif k in ("admin", "deactivated"):
        value = human_readable_bool(user_dict[k])
    elif k.endswith("_ts"):
        value = str(
            datetime.datetime.fromtimestamp(float(user_dict[k]))
        )  # UTC?
    elif k.endswith("_at"):
        value = str(
            datetime.datetime.fromtimestamp(float(user_dict[k]) / 1000.0)
        )  # UTC?

    else:
        value = user_dict[k]

    if key is None:
        key = k.replace("_", " ").title()

    return key, value


def generate_user_tables(
    user_dict: Dict[str, Any], len_domain: int
) -> List[List[Tuple[str, str]]]:
    """Generate a main user table and threepid user tables.

    The function gnerates first a main user table and then for every threepid
    a additional table from a ``user_dict``.
    It renames and makes the output human readable.

    This function is a recursive function

    :param user_dict:   A JSON string which was converted to a Python
                        dictionary.
    :param len_domain:  The length in characters of the domain.
    :return:            The generated lists in this format:
                        [main], threepids_0, ... ,threepids_n]
    """

    table: List[List[Tuple[str, str]]] = [[]]

    for k in user_dict:
        if k == "errcode":
            error("There is no user with that username.")
            sys.exit(1)

        if k == "threepids":
            for tk in user_dict[k]:
                ret: List[List[Tuple[str, str]]] = generate_user_tables(
                    tk, len_domain
                )
                table.append(ret[0])

            continue  # Don't add threepids to "table"

        table[0].append(make_human_readable(k, user_dict, len_domain))

    return table


def user(arg: Namespace) -> int:
    """List information about an registered user.

    It uses the admin API to get a python dictionary with the information.
    The ``generate_user_tables`` function makes the information human readable.
    The Python package ``tabulate`` renders the table as shown below, if
    everything works well.


    .. code-block:: console

       $ matrixctl user dwight
       User:
       +----------------------------+--------------------------------------+
       | Name                       | dwight                               |
       | Password Hash              | $2b$12$9DUNderm1ffL1NincPap3RC       |
       |                            | ompaNY1725.slOUghAvEnu5cranT0n       |
       | Guest                      | False                                |
       | Admin                      | True                                 |
       | Consent Version            |                                      |
       | Consent Server Notice Sent |                                      |
       | Appservice Id              |                                      |
       | Creation Ts                | 2020-04-14 13:04:21                  |
       | User Type                  |                                      |
       | Deactivated                | False                                |
       | Displayname                | Dwight Schrute                       |
       | Avatar Url                 | mxc://dunder-mifflin.com/sCr4        |
       |                            | nt0nsr4ng13rW45Cr33d                 |
       +----------------------------+--------------------------------------+

       Threepid:
       +--------------+-----------------------------------+
       | Medium       | email                             |
       | Address      | dwight_schrute@dunder-mifflin.com |
       | Validated At | 2020-04-14 15:30:21.123000        |
       | Added At     | 2020-04-14 15:29:19.100000        |
       +--------------+-----------------------------------+


    If the user does not exist, the return looks like:


    .. code-block:: console

       $ matrixctl user mose
       2020-04-14 13:58:13 - ERROR - The request was not successful.
       2020-04-14 13:58:13 - ERROR - There is no user with that username.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param cfg:       The ``Config`` class
    :return:          None
    """

    with TOML() as toml:
        with API(
            toml.get(("API", "Domain")), toml.get(("API", "Token"))
        ) as api:
            api.url.path = f'users/@{arg.user}:{toml.get(("API","Domain"))}'

            try:
                user_dict: JsonDict = api.request().json()
            except InternalResponseError:
                fatal("Could not receive the user information")

                return 1

            len_domain = len(toml.get(("API", "Domain"))) + 1  # 1 for :
            user_tables = generate_user_tables(user_dict, len_domain)

            debug(f"User: {user_tables=}")

            for num, table in enumerate(user_tables):

                if num < 1:
                    print("User:")
                else:
                    print("\nThreepid:")
                print(
                    tabulate(
                        table,
                        tablefmt="psql",
                    )
                )

    return 0


# vim: set ft=python :
