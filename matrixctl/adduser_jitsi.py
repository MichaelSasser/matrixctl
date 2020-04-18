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

from argparse import ArgumentParser, Namespace
from argparse import _SubParsersAction as SubParsersAction

from .handlers.config import Config
from .handlers.ssh import SSH
from .password_helpers import ask_password, ask_question, gen_password

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


JID_EXT: str = "matrix-jitsi-web"


def subparser_adduser_jitsi(subparsers: SubParsersAction) -> None:
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


def adduser_jitsi(arg: Namespace, cfg: Config) -> int:
    """Add a User to the jitsi instance.

    It runs ``ask_password()``
    first. If ``ask_password()`` returns ``None`` it generates a password
    with ``gen_password()``. Then it gives the user a overview of the
    username, password and if the new user should be generated as admin
    (if you added the ``--admin`` argument). Next, it asks a question,
    if the entered values are correct with the ``ask_question`` function.

    If the ``ask_question`` function returns True, it continues. If not, it
    starts from the beginning.

    It runs the ``adduser`` method of the ``Ssh`` class.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param cfg:       The ``Config`` class
    :return:          None
    """

    with SSH(cfg.api_domain) as ssh:
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
            f"--config /config/prosody.cfg.lua register"
            f'"{arg.user} {JID_EXT} "{arg.password}"'
        )

        ssh.run_cmd(cmd)

        return 0
        # res: SSHResponese = ssh.run_cmd(cmd)

        # ToDo:
        # if res.stderr.startswith("???"):
        #     error(
        #         "BUG: It's likely that you had previously installed Jitsi "
        #         "without auth/guest support. Please look into the "
        #         "configuring-playbook-jitsi.md in "
        #         "matrix-docker-ansible-deploy/docs. Read the paragraph "
        #         "about rebuilding your Jitsi installation."
        #     )
        #     sys.exit(1)


# vim: set ft=python :
