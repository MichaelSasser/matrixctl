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


"""Use this module to add the ``adduser-jitsi`` subcommand to ``matrixctl``."""

from __future__ import annotations

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction

from .handlers.ssh import SSH
from .handlers.toml import TOML
from .password_helpers import ask_password
from .password_helpers import ask_question
from .password_helpers import gen_password


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


JID_EXT: str = "matrix-jitsi-web"


def subparser_adduser_jitsi(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl adduser-jitsi`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "adduser-jitsi", help="Add a new jitsi user"
    )
    parser.add_argument("user", help="The Username of the new jitsi user")
    parser.add_argument(
        "-p",
        "--passwd",
        help="The password of the new jitsi user. (If you don't enter a "
        "password, you will be asked later.)",
    )
    parser.set_defaults(func=adduser_jitsi)


def adduser_jitsi(arg: Namespace) -> int:
    """Add a User to the jitsi instance.

    It runs ``ask_password()`` first. If ``ask_password()`` returns ``None``
    it generates a password with ``gen_password()``. Then it gives the user
    a overview of the username, password and if the new user should be
    generated as admin (if you added the ``--admin`` argument). Next, it asks
    a question, if the entered values are correct with the ``ask_question``
    function.

    If the ``ask_question`` function returns True, it continues. If not, it
    starts from the beginning.

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
    address = (
        toml.get("SSH", "Address")
        if toml.get("SSH", "Address")
        else f"matrix.{toml.get('API', 'Domain')}"
    )
    with SSH(address, toml.get("SSH", "User"), toml.get("SSH", "Port")) as ssh:
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

            answer = ask_question()

            if answer:
                break
            arg.passwd = None

        cmd: str = (
            "sudo docker exec matrix-jitsi-prosody prosodyctl "
            f"--config /config/prosody.cfg.lua register "
            f'"{arg.user}" {JID_EXT} "{arg.passwd}"'
        )

        ssh.run_cmd(cmd)

        return 0


# vim: set ft=python :
