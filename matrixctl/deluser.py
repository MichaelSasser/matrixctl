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

"""Use this module to add the ``deluser`` subcommand to ``matrixctl``."""

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


def subparser_deluser(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl deluser`` command.

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
        "deluser", help="Deletes a user"
    )
    parser.add_argument("user", help="The username to delete")
    parser.set_defaults(func=deluser)


def deluser(arg: Namespace) -> int:
    """Delete a user from the the matrix instance.

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
        path=f"deactivate/@{arg.user}:{toml.get('API','Domain')}",
        api_version="v1",
        method="POST",
        data={"erase": True},
    )
    try:
        request(req)
    except InternalResponseError:
        logger.error("The user was not deleted.")

    return 0


# vim: set ft=python :
