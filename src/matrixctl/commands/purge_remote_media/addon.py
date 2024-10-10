# matrixctl
# Copyright (c) 2021-2023  Michael Sasser <Michael@MichaelSasser.org>
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
from datetime import timezone

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

    timestamp = handle_timestamp(arg.timestamp, force=arg.force)

    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path="/_synapse/admin/v1/purge_media_cache",
        params={"before_ts": timestamp},
        method="POST",
        timeout=1200,
    )

    try:
        response: Response = request(req)
    except InternalResponseError:
        logger.exception("The user could not be promoted or demote.")
        return 1

    try:
        json_response: JsonDict = response.json()
    except json.decoder.JSONDecodeError as e:
        logger.exception("The JSON response could not be loaded by MatrixCtl.")
        msg = f"The response was: {response = }"
        raise InternalResponseError(msg) from e

    if arg.to_json:
        try:
            print(json.dumps(json_response, indent=4))
        except json.decoder.JSONDecodeError:
            logger.exception("Unable to process the response data to JSON.")
            return 1
    else:
        print(f"Deleted Media Files: {json_response['deleted']}")

    return 0


def handle_timestamp(timestamp: int | None, *, force: bool) -> int:
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
    ts: float = (datetime.now(tz=timezone.utc) - timedelta(days=7)).timestamp()
    if timestamp is None:
        if not force:
            print(
                "You are about to delete all remote media, that wasn't "
                "accessed in the last seven days",
            )
            if not ask_question("Do you want to continue?"):
                sys.exit(0)
        return int(round(ts * 1000))
    try:
        dt = datetime.fromtimestamp(float(timestamp) / 1000, tz=timezone.utc)
        logger.info("Delete until dt = %s", dt)
    except (OverflowError, OSError, ValueError):
        logger.fatal(
            "The argument timestamp = %s is not a valid timestamp.",
            timestamp,
        )
    return timestamp


# vim: set ft=python :
