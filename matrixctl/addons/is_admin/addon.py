#!/usr/bin/env python
# matrixctl
# Copyright (c) 2021  Michael Sasser <Michael@MichaelSasser.org>
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

"""Use this module to add the ``is-admin`` subcommand to ``matrixctl``."""

from __future__ import annotations

import json
import logging

from argparse import Namespace

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import Response
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.print_helpers import human_readable_bool
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Delete a user is an admin.

    Notes
    -----
    If a user does not exist it still will return ``"admin": false`` or ``No``.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``
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
        path=f"users/@{arg.user}:{yaml.get('server', 'api','domain')}/admin",
        api_version="v1",
        method="GET",
    )
    try:
        response: Response = request(req)
    except InternalResponseError:
        logger.error("The user could not be checked.")
        return 1

    response_json: JsonDict = response.json()

    if arg.to_json:
        print(json.dumps(response_json, indent=4))
        return 0

    print(human_readable_bool(response_json["admin"]))
    return 0


# vim: set ft=python :
