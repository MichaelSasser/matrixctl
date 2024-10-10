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

"""Use this module to list an approximation of the largest rooms."""

from __future__ import annotations

import json
import logging

from argparse import Namespace

from .to_table import to_table

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import Response
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

DEFAULT_LIMIT: int = 100


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Generate a table of the top 10 matrix rooms in terms of DB storage.

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
        path="/_synapse/admin/v1/statistics/database/rooms",
    )

    try:
        response: Response = request(req)
    except InternalResponseError:
        logger.critical("Could not get top 10 rooms in terms of DB storage.")
        return 1
    response_json: JsonDict = response.json()

    generate_output(
        response_json["rooms"],
        to_json=arg.to_json,
    )

    return 0


def generate_output(rooms: list[JsonDict], *, to_json: bool) -> None:
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
