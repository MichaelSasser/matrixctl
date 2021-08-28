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

"""Use this module to add the ``users`` subcommand to ``matrixctl``."""

from __future__ import annotations

import json
import logging

from argparse import Namespace

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict

from .to_table import to_table


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


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
    len_domain = len(yaml.get("api", "domain")) + 1  # 1 for :
    from_user: int = 0
    users_list: list[JsonDict] = []

    # ToDo: API bool
    req: RequestBuilder = RequestBuilder(
        token=yaml.get("api", "token"),
        domain=yaml.get("api", "domain"),
        path="users",
        api_version="v2",
        params={
            "guests": "true" if arg.with_guests or arg.all else "false",
            "deactivated": "true"
            if arg.with_deactivated or arg.all
            else "false",
        },
    )

    while True:

        req.params["from"] = from_user  # from must be in the loop
        try:
            lst: JsonDict = request(req).json()
        except InternalResponseError:
            logger.critical("Could not get the user table.")

            return 1

        users_list += lst["users"]

        try:
            from_user = lst["next_token"]
        except KeyError:
            break
    if arg.to_json:
        print(json.dumps(users_list, indent=4))
    else:
        for line in to_table(users_list, len_domain):
            print(line)

    return 0


# vim: set ft=python :
