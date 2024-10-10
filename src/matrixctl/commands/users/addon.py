# matrixctl
# Copyright (c) 2020-2023  Michael Sasser <Michael@MichaelSasser.org>
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

"""Use this module to add the ``users`` subcommand to ``matrixctl``."""

from __future__ import annotations

import json
import logging

from argparse import Namespace
from contextlib import suppress

from .to_table import to_table

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import Response
from matrixctl.handlers.api import generate_worker_configs
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

DEFAULT_LIMIT: int = 100

logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Print a table/json of the matrix users.

    This function generates and prints a table of users or uses json as
    output format.

    The table can be modified.

    - If you want guests in the table use the ``--with-guests`` switch.
    - If you want deactivated user in the table use the ``--with-deactivated``
      switch.

    Notes
    -----
    - Needs API version 2 (``synapse`` 1.28 or greater) to work.
    - API version 1 is deprecated. If you encounter problems please upgrade
      to the latest ``synapse`` release.

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
    len_domain = len(yaml.get("server", "api", "domain")) + 1  # 1 for :
    users: list[JsonDict] = []
    next_token: int | None = None
    total: int | None = None

    # TODO: API bool
    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path="/_synapse/admin/v2/users",
        method="GET",
        params={
            "guests": "true" if arg.with_guests or arg.all else "false",
            "from": 0,
            "limit": (
                arg.limit if 0 < arg.limit < DEFAULT_LIMIT else DEFAULT_LIMIT
            ),
            "deactivated": (
                "true" if arg.with_deactivated or arg.all else "false"
            ),
        },
        timeout=10,
        concurrent_limit=yaml.get("server", "api", "concurrent_limit"),
    )

    try:
        response: Response = request(req)
    except InternalResponseError:
        logger.critical("Could not get the data do build the user table.")
        return 1
    response_json: JsonDict = response.json()

    users += response_json["users"]

    with suppress(KeyError):  # Done: No more users
        next_token = int(response_json["next_token"])
        total = int(response_json["total"])
        if 0 < arg.limit < total:
            total = arg.limit

    # New group to not suppress KeyError in here
    if next_token is not None and total is not None and total > DEFAULT_LIMIT:
        async_responses = request(
            generate_worker_configs(req, next_token, total),
        )

        for async_response in async_responses:
            users_list = async_response.json()["users"]
            for user in users_list:
                users.append(user)

    if arg.to_json:
        print(json.dumps(users, indent=4))
    else:
        for line in to_table(users, len_domain):
            print(line)
        print(f"Total number of users: {len(users)}")

    return 0


# vim: set ft=python :
