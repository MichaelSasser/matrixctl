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

"""Use this module to add the ``delroom`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction

from .errors import InternalResponseError
from .handlers.api import RequestBuilder
from .handlers.api import request
from .handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def subparser_delroom(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl delroom`` command.

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
        "delroom", help="Deletes an empty room from the database"
    )
    parser.add_argument(
        "RoomID",
        type=str,
        help="The Room-ID",
    )
    parser.set_defaults(func=delroom)


def delroom(arg: Namespace) -> int:
    """Delete an empty room from the database.

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
    req: RequestBuilder = RequestBuilder(
        token=toml.get("API", "Token"),
        domain=toml.get("API", "Domain"),
        path="purge_room",
        method="POST",
        api_version="v1",
        data={"room_id": arg.RoomID},
    )

    try:
        request(req).json()
    except InternalResponseError as e:
        if "json" in dir(e.payload):
            try:
                if e.payload.json()["errcode"] in (
                    "M_NOT_FOUND",
                    "M_UNKNOWN",
                ):
                    logger.error(f"{e.payload.json()['error']}")

                    return 1
            except KeyError:
                pass  # log the fallback error

        logger.error("Could not delete room")

        return 1

    return 0


# vim: set ft=python :
