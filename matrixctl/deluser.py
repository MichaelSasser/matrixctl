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
from .api_handler import Api

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_deluser(subparsers):
    deluser_parser = subparsers.add_parser("deluser", help="Deletes a user")
    deluser_parser.add_argument("user", help="The username to delete")
    deluser_parser.set_defaults(func=deluser)


def deluser(arg: Namespace, cfg: Config) -> None:
    """This function deletes a user from the matrix instance.
    It uses the synapse admin API.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param _:         Not used (The ``Config`` class)
    :return:          None
    """
    with Api(cfg.api_domain, cfg.api_token) as api:
        api.deluser(arg.user)


# vim: set ft=python :
