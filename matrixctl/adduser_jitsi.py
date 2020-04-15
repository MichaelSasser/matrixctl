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
from .password_helpers import ask_password, gen_password, ask_question
from .config_handler import Config
from .ssh_handler import Ssh

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_adduser_jitsi(subparsers):
    adduser_jitsi_parser = subparsers.add_parser(
        "adduser-jitsi", help="Add a new jitsi user"
    )
    adduser_jitsi_parser.add_argument(
        "user", help="The Username of the new jitsi user"
    )
    adduser_jitsi_parser.add_argument(
        "-p",
        "--passwd",
        help="The password of the new jitsi user. (If you don't enter a "
        "password, you will be asked later.)",
    )
    adduser_jitsi_parser.set_defaults(func=adduser_jitsi)


def adduser_jitsi(arg: Namespace, cfg: Config) -> None:
    """Adds a User to the jitsi instance. It runs ``ask_password()``
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
            print(f"Password: **HIDDEN**")

        answer = ask_question()

        if answer:
            break
        arg.passwd = None

    with Ssh(cfg) as ssh:
        ssh.adduser(arg.user, arg.passwd)


# vim: set ft=python :
