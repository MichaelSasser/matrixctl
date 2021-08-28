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
    from_event: int = 0
    events_raw: list[JsonDict] = []

    # ToDo: API bool
    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path="event_reports",
        api_version="v1",
    )

    while True:

        req.params["from"] = from_event  # from must be in the loop
        try:
            response: JsonDict = request(req).json()
        except InternalResponseError:
            logger.critical("Could not get the event_reports table.")

            return 1

        events_raw += response["event_reports"]

        try:
            from_event = response["next_token"]
        except KeyError:
            break

    if arg.to_json:
        print(json.dumps(events_raw, indent=4))
    else:
        for line in to_table(events_raw):
            print(line)

    return 0


# vim: set ft=python :
