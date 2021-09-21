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

"""Use this module to add the ``rooms`` subcommand to ``matrixctl``."""

from __future__ import annotations

import json
import logging

from argparse import Namespace
from contextlib import suppress

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import Response
from matrixctl.handlers.api import generate_worker_configs
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict

from .to_table import to_table


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Generate a table of the matrix rooms.

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
    rooms: list[JsonDict] = []
    next_token: int | None = None
    total: int | None = None

    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path="rooms",
        api_version="v1",
        params={"limit": arg.limit if 0 < arg.limit < 100 else 100},
        concurrent_limit=yaml.get("server", "api", "concurrent_limit"),
    )

    if arg.filter:
        req.params["search_term"] = arg.filter

    if arg.reverse:
        req.params["dir"] = "b"

    if arg.order_by_size:
        req.params["order_by"] = "size"

    try:
        response: Response = request(req)
    except InternalResponseError:
        logger.critical("Could not get the user table.")
        return 1
    response_json: JsonDict = response.json()

    rooms += response_json["rooms"]

    with suppress(KeyError):  # Done: No more users
        next_token = int(response_json["next_batch"])
        total = int(response_json["total_rooms"])
        if 0 < arg.limit < total:
            total = arg.limit

    # New group to not suppress KeyError in here
    if next_token is not None and total is not None and total > 100:
        async_responses = request(
            generate_worker_configs(req, next_token, total),
            concurrent_limit=req.concurrent_limit,
        )

        for async_response in async_responses:
            users_list = async_response.json()["rooms"]
            for room in users_list:
                rooms.append(room)

    generate_output(rooms, arg.to_json)

    return 0


# Add limit


def generate_output(rooms: list[JsonDict], to_json: bool) -> None:
    """Use this helper to generate the output.

    Parameters
    ----------
    rooms : list of matrixctl.typehints.JsonDict
        A list of rooms from the API.
    to_json : bool
        ``True``, when the output should be in the JSON format.
        ``False``, when the output should be a table.

    Returns
    -------
    None

    """
    if to_json:
        print(json.dumps(rooms, indent=4))
    else:
        for line in to_table(rooms):
            print(line)
        print(f"Total number of rooms: {len(rooms)}")


# vim: set ft=python :
