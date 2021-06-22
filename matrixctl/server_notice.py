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

"""Use this module to add the ``serve-notice`` subcommand to ``matrixctl``."""

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


def subparser_server_notice(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl server-notice`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "server-notice", help="Send a server notice"
    )
    parser.add_argument(
        "username",
        help=(
            "The user which will receive the server-notice."
            "(e.g. for '@Michael@MichaelSasser.org' use 'michael')"
        ),
    )
    parser.add_argument("message", help="The message")
    parser.set_defaults(func=server_notice)


def server_notice(arg: Namespace) -> int:
    """Send a server notice to a matrix instance.

    Notes
    -----
    - It uses the synapse admin API.
    - Note that "server notices" must be enabled in homeserver.yaml before
      this API can be used.

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
    req: RequestBuilder = RequestBuilder(
        token=toml.get("API", "Token"),
        domain=toml.get("API", "Domain"),
        path="send_server_notice",
        method="POST",
        api_version="v1",
        data={
            "user_id": (f"@{arg.username}:" f"{toml.get('API', 'Domain')}"),
            "content": {
                "msgtype": "m.text",
                "body": arg.message,
            },
        },
    )

    try:
        request(req)
    except InternalResponseError:
        logger.error("The server notice was not sent.")

    return 0


# vim: set ft=python :
