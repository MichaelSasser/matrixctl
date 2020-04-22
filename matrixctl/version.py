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
from logging import debug
from logging import error
from logging import fatal

from .errors import InternalResponseError
from .handlers.api import API
from .handlers.toml import TOML
from .typing import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_version(subparsers: SubParsersAction) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "version", help="Get the version of the Synapse instance"
    )
    parser.set_defaults(func=version)


def version(_: Namespace) -> int:
    """Get the version of the Synapse instance.

    :param _:  The ``Namespace`` object of argparse's ``arse_args()``
    :return:   None
    """
    with TOML() as toml:
        with API(
            toml.get(("API", "Domain")), toml.get(("API", "Token"))
        ) as api:
            api.url.path = "server_version"
            api.url.api_version = "v1"
            try:
                response: JsonDict = api.request().json()
            except InternalResponseError:
                fatal("Could not get the server sersion.")

                return 1
            debug(f"{response=}")
            try:
                print(f"Server Version: {response['server_version']}")
                print(f"Python Version: {response['python_version']}")
            except KeyError:
                error("MatrixCtl was not able to read the server version.")

    return 0


# vim: set ft=python :
