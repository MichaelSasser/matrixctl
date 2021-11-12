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

import json
import logging

from argparse import Namespace

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import Response
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Delete an empty room from the database.

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
    body: JsonDict = handle_arguments(arg)

    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path=f"rooms/{arg.room}",
        method="DELETE",
        api_version="v1",
        json=body,
        timeout=1200,
    )

    try:
        response: Response = request(req)
    except InternalResponseError:
        logger.error("Could not delete room.")
        return 1

    try:
        json_response: JsonDict = response.json()
    except json.decoder.JSONDecodeError as e:
        logger.fatal("The JSON response could not be loaded by MatrixCtl.")
        raise InternalResponseError(f"The response was: {response = }") from e

    print(json.dumps(json_response, indent=4))

    return 0


def handle_arguments(arg: Namespace) -> JsonDict:
    """Build the parameters used for the delroom request.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``

    Returns
    -------
    body : matrixctl.typehints.JsonDict
        The params.

    """
    body: JsonDict = {
        "block": arg.block,
        "purge": arg.no_purge,
    }
    if arg.new_room_admin is not None:
        body["new_room_user_id"] = arg.new_room_admin
        body["room_name"] = arg.new_room_name
        if arg.message is None:
            body["message"] = (
                f"{arg.room} has been shutdown due to content violations "
                "on this server. Please review our Terms of Service."
            )
        else:
            body["message"] = arg.message

    return body


# vim: set ft=python :
