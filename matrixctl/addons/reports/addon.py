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

"""Use this module to add the ``reports`` subcommand to ``matrixctl``."""

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
    """Print a table/json of the reported events.

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
    reports: list[JsonDict] = []
    next_token: int | None = None
    total: int | None = None

    # ToDo: API bool
    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path="event_reports",
        api_version="v1",
        params={
            "from": 0,
            "limit": arg.limit if 0 < arg.limit < 100 else 100,
        },
        concurrent_limit=yaml.get("server", "api", "concurrent_limit"),
    )

    try:
        response: Response = request(req)
    except InternalResponseError:
        logger.critical("Could not get the data do build the user table.")
        return 1
    response_json: JsonDict = response.json()

    reports += response_json["event_reports"]

    with suppress(KeyError):  # Done: No more users
        next_token = int(response_json["next_token"])
        total = int(response_json["total"])
        if 0 < arg.limit < total:
            total = arg.limit

    # New group to not suppress KeyError in here
    if next_token is not None and total is not None and total > 100:
        async_responses = request(
            generate_worker_configs(req, next_token, total),
            concurrent_limit=req.concurrent_limit,
        )

        for async_response in async_responses:
            reports_list = async_response.json()["event_reports"]
            for report in reports_list:
                reports.append(report)

    if arg.to_json:
        print(json.dumps(reports, indent=4))
    else:
        for line in to_table(reports):
            print(line)

    return 0


# vim: set ft=python :
