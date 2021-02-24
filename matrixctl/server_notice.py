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
from logging import error

from .errors import InternalResponseError
from .handlers.api import API
from .handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_server_notice(subparsers: SubParsersAction) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "server-notice", help="Send a server notice"
    )
    parser.add_argument("message", help="The message")
    parser.set_defaults(func=server_notice)


def server_notice(arg: Namespace) -> int:
    """Send a server notice to a matrix instance.

    It uses the synapse admin API.
    Note that server notices must be enabled in homeserver.yaml before
    this API can be used.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param _:         Not used (The ``Config`` class)
    :return:          None
    """
    with TOML() as toml:
        with API(
            toml.get(("API", "Domain")), toml.get(("API", "Token"))
        ) as api:
            request = {
                "user_id": (
                    f"@{toml.get(('API', 'Username'))}:"
                    f"{toml.get(('API', 'Domain'))}"
                ),
                "content": {
                    "msgtype": "m.text",
                    "body": arg.message,
                },
            }

            try:
                api.url.path = "send_server_notice"
                api.url.api_version = "v1"
                api.method = "POST"
                api.request(request)
            except InternalResponseError:
                error("The server notice was not sent.")

        return 0


# vim: set ft=python :
