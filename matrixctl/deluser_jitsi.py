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
from .handlers.ssh import SSH

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


JID_EXT: str = "matrix-jitsi-web"


def subparser_deluser_jitsi(subparsers):
    parser = subparsers.add_parser(
        "deluser-jitsi", help="Deletes a jitsi user"
    )
    parser.add_argument("user", help="The jitsi username to delete")
    parser.set_defaults(func=deluser_jitsi)


def deluser_jitsi(arg: Namespace, cfg: Config) -> None:
    """This function deletes a user from the jitsi instance.
    It uses the ``Ssh`` class from the ``ssh_handler``.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param cfg:       The ``Config`` class
    :return:          None
    """
    with SSH(cfg) as ssh:
        cmd: str = (
            "sudo docker exec matrix-jitsi-prosody prosodyctl "
            "--config /config/prosody.cfg.lua deluser "
            f'"{arg.user}@{JID_EXT}"'
        )

        ssh.run_cmd(cmd)


# vim: set ft=python :
