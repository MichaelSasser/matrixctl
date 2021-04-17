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

"""Use this module to add the ``adduser`` subcommand to ``matrixctl``."""

from __future__ import annotations

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction
from logging import error

from .errors import InternalResponseError
from .handlers.ansible import ansible_run
from .handlers.api import API
from .handlers.toml import TOML
from .password_helpers import ask_password
from .password_helpers import ask_question
from .password_helpers import gen_password


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_adduser(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl adduser`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by
        ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "adduser", help="Add a new matrix user"
    )
    parser.add_argument("user", help="The Username of the new user")
    parser.add_argument(
        "-p",
        "--passwd",
        help="The password of the new user. (If you don't enter a password, "
        "you will be asked later.)",
    )
    parser.add_argument(
        "-a", "--admin", action="store_true", help="Create as admin user"
    )
    parser.add_argument(
        "--ansible", action="store_true", help="Use ansible insted of the api"
    )
    parser.set_defaults(func=adduser)


def adduser(arg: Namespace) -> int:
    """Add a User to the synapse instance.

    It runs ``ask_password()`` first. If ``ask_password()`` returns ``None``
    it generates a password with ``gen_password()``. Then it gives the user
    a overview of the username, password and if the new user should be
    generated as admin (if you added the ``--admin`` argument). Next, it asks
    a question, if the entered values are correct with the ``ask_question``
    function.

    If the ``ask_question`` function returns True, it continues. If not, it
    starts from the beginning.

    Depending on the ``--ansible`` switch it runs the ``adduser`` command
    via ansible or the API

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """

    toml: TOML = TOML()
    api: API = API(toml.get("API", "Domain"), toml.get("API", "Token"))

    while True:
        passwd_generated: bool = False

        if arg.passwd is None:
            arg.passwd = ask_password()

        if arg.passwd == "":
            arg.passwd = gen_password()
            passwd_generated = True

        print(f"Username: {arg.user}")

        if passwd_generated:
            print(f"Password (generated): {arg.passwd}")
        else:
            print("Password: **HIDDEN**")
        print(f"Admin:    {'yes' if arg.admin else 'no'}")

        answer = ask_question()

        if answer:
            break
        arg.passwd = None

    if arg.ansible:
        ansible_run(
            playbook=toml.get("ANSIBLE", "Playbook"),
            tags="register-user",
            extra_vars={
                "username": arg.user,
                "password": arg.passwd,
                "admin": "yes" if arg.admin else "no",
            },
        )
    else:
        try:
            api.url.path = f"users/@{arg.user}:{toml.get('API','Domain')}"
            api.method = "PUT"
            api.request({"password": arg.passwd, "admin": arg.admin})
        except InternalResponseError:
            error("The User was not added.")

    return 0


# vim: set ft=python :
