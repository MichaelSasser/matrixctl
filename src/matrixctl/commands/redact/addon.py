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

"""Use this module to add the ``delroom`` subcommand to ``matrixctl``."""

from __future__ import annotations

import json
import logging
import typing as t

from argparse import Namespace
from time import sleep

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import Response
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.sanitizers import sanitize_room_identifier
from matrixctl.sanitizers import sanitize_sequence
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Redact events of a given user.

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
    body: JsonDict | t.Literal[1] = handle_arguments(arg)
    if isinstance(body, int):
        return body

    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path=f"/_synapse/admin/v1/user/{arg.user_id}/redact",
        method="POST",
        json=body,
        timeout=1200,
    )

    try:
        response: Response = request(req)
    except InternalResponseError:
        logger.exception("Could not redact events.")
        return 1

    try:
        json_response: JsonDict = response.json()
    except json.decoder.JSONDecodeError as e:
        logger.fatal("The JSON response could not be loaded by MatrixCtl.")
        msg: str = f"The response was: {response = }"
        raise InternalResponseError(msg) from e

    try:
        json_response = handle_status(
            yaml,
            json_response["redact_id"],
        )
    except InternalResponseError as e:
        if e.message:
            logger.fatal(e.message)
        logger.fatal(
            "MatrixCtl was not able to verify the status of the request.",
        )
        return 1

    print(json.dumps(json_response, indent=4))

    return 0


# TODO: Try to simplify this function
# ruff: noqa: C901
def handle_status(yaml: YAML, redact_id: str) -> JsonDict:
    """Handle the status of a delete room request.

    Parameters
    ----------
    yaml : matrixctl.handlers.yaml.YAML
        The configuration file handler.
    delete_id: str
        The delete id of a delete room request.

    Returns
    -------
    response: matrixctl.typehints.JsonDict, optional
        The response as dict, containing the status.

    """
    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path=f"/_synapse/admin/v1/user/redact_status/{redact_id}",
        method="GET",
        timeout=1200.0,
    )

    # Lock messages to only print them once
    msglock_scheduled: bool = False  # TODO: rly needed here?
    msglock_active: bool = False

    while True:
        sleep(1)
        try:
            response: Response = request(req)
        except InternalResponseError as e:
            msg: str = (
                "The delete room request was probably successful but the"
                " status request failed. You just have to wait a bit."
            )
            raise InternalResponseError(msg) from e

        try:
            json_response: JsonDict = response.json()
        except json.decoder.JSONDecodeError as e:
            logger.fatal(
                "The JSON status response could not be loaded by MatrixCtl.",
            )
            msg_: str = f"The response was: {response = }"
            raise InternalResponseError(msg_) from e

        if response is not None:
            logger.debug("response: %s", response)
            # complete
            if json_response["status"] == "completed":
                print(
                    "Status: Complete "
                    "(The Events have been redacted successfully)",
                )
                break
            # scheduled
            if json_response["status"] == "scheduled":
                if not msglock_scheduled:
                    print(
                        "Status: Scheduled "
                        "(The Redaction Progress Will Start Soon)",
                    )
                msglock_scheduled = True
                logger.info(
                    "The server is still shutting_down the room. "
                    "Please wait...",
                )
                sleep(5)
                continue
            # purging
            if json_response["status"] == "active":
                if not msglock_active:
                    print("Status: Active (Redacting Events)")
                msglock_active = True
                logger.info(
                    "The server is still purging the room. Please wait...",
                )
                sleep(5)
                continue
            # failed
            if json_response["status"] == "failed":
                logger.critical(
                    (
                        "The server returned, that the approach failed with "
                        "the following message: %s."
                    ),
                    json_response["status"],
                )
                break
        break

    return json_response


def handle_arguments(arg: Namespace) -> JsonDict | t.Literal[1]:
    """Build the parameters used for the redact request.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``

    Returns
    -------
    body : matrixctl.typehints.JsonDict
        The params.

    """

    room_identifiers: tuple[str, ...] | t.Literal[False] | None = (
        sanitize_sequence(sanitize_room_identifier, arg.room_ids)
    )
    if room_identifiers is False:
        return 1

    body: JsonDict = {
        "rooms": room_identifiers,
        "reason": arg.reason.strip(),
        "limit": arg.limit,
    }

    logger.debug("Body: %s", body)
    return body


# vim: set ft=python :
