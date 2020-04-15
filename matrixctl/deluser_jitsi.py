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
from .config_handler import Config
from .ssh_handler import Ssh

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_deluser_jitsi(subparsers):
    deluser_jitsi_parser = subparsers.add_parser(
        "deluser-jitsi", help="Deletes a jitsi user"
    )
    deluser_jitsi_parser.add_argument(
        "user", help="The jitsi username to delete"
    )
    deluser_jitsi_parser.set_defaults(func=deluser_jitsi)


def deluser_jitsi(arg: Namespace, cfg: Config) -> None:
    """This function deletes a user from the jitsi instance.
    It uses the ``Ssh`` class from the ``ssh_handler``.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param cfg:       The ``Config`` class
    :return:          None
    """
    with Ssh(cfg) as ssh:
        ssh.deluser(arg.user)


# vim: set ft=python :
