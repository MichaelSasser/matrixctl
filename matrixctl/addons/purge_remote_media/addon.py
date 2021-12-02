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

"""Use this module to delete remote media."""

from __future__ import annotations

import json
import logging
import sys

from argparse import Namespace
from datetime import datetime
from datetime import timedelta

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import Response
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.password_helpers import ask_question
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Remove remote media.

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

    timestamp = handle_timestamp(arg.timestamp, arg.force)

    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path="purge_media_cache",
        params={"before_ts": timestamp},
        api_version="v1",
        method="POST",
        timeout=1200,
    )

    try:
        response: Response = request(req)
    except InternalResponseError:
        logger.error("The user could not be promoted or demote.")
        return 1

    try:
        json_response: JsonDict = response.json()
    except json.decoder.JSONDecodeError as e:
        logger.fatal("The JSON response could not be loaded by MatrixCtl.")
        raise InternalResponseError(f"The response was: {response = }") from e

    if arg.to_json:
        try:
            print(json.dumps(json_response, indent=4))
            return 0
        except json.decoder.JSONDecodeError:
            logger.error("Unable to process the response data to JSON.")
            return 1
    else:
        print(f"Deleted Media Files: {json_response['deleted']}")

    return 0


def handle_timestamp(timestamp: int | None, force: bool) -> int:
    """Ask or generate timestamp.

    Parameters
    ----------
    timestamp : int, optional
        The timestamp
    force : bool
        Don't ask any questions. All questions are answered with ``True``.

    Returns
    -------
    timestamp : int
        The same timestamp but sanitized, or the timestamp of this exact time.

    """
    ts: float = (datetime.today() - timedelta(days=7)).timestamp()
    if timestamp is None:
        if not force:
            print(
                "You are about to delete all remote media, that wasn't "
                "accessed in the last seven days"
            )
            if not ask_question("Do you want to continue?"):
                sys.exit(0)
        return int(round(ts * 1000))
    try:
        dt = datetime.fromtimestamp(float(timestamp) / 1000)
        logger.info(f"Delete until {dt=}")
    except (OverflowError, OSError, ValueError):
        logger.fatal(
            f"The argument timestamp = {timestamp} is not a valid timestamp."
        )
    return timestamp


# vim: set ft=python :
