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

from argparse import Namespace

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
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
    yaml : matrixctl.handlers.yaml.YAML
        The configuration file handler.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path="send_server_notice",
        method="POST",
        api_version="v1",
        data={
            "user_id": (
                f"@{arg.username}:" f"{yaml.get('server', 'api', 'domain')}"
            ),
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
