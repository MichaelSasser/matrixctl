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


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Print a table of the reported events.

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
        path=f"event_reports/{arg.report_id}",
        api_version="v1",
    )

    try:
        response: JsonDict = request(req).json()
    except InternalResponseError:
        logger.critical("Could not receive the user information")

        return 1

    try:
        print(json.dumps(response, indent=4))
        return 0
    except json.decoder.JSONDecodeError:
        logger.error("Unable to process the response data to JSON.")
        return 1
    return 0


# vim: set ft=python :
