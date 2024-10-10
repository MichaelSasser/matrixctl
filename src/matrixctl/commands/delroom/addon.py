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

from argparse import Namespace
from time import sleep

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import Response
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Delete an empty room from the database.

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
    body: JsonDict = handle_arguments(arg)

    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path=f"/_synapse/admin/v2/rooms/{arg.room}",
        method="DELETE",
        json=body,
        timeout=1200,
    )

    try:
        response: Response = request(req)
    except InternalResponseError:
        logger.exception("Could not delete room.")
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
            json_response["delete_id"],
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
def handle_status(yaml: YAML, delete_id: str) -> JsonDict:
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
        path=f"/_synapse/admin/v2/rooms/delete_status/{delete_id}",
        method="GET",
        timeout=1200.0,
    )

    # Lock messages to only print them once
    msglock_shutting_down: bool = False
    msglock_purging: bool = False

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
            if json_response["status"] == "complete":
                print(
                    "Status: Complete (the room has been deleted"
                    "successfully)",
                )
                break
            # shutting_down
            if json_response["status"] == "shutting_down":
                if not msglock_shutting_down:
                    print(
                        "Status: Shutting Down (removing users from the room)",
                    )
                msglock_shutting_down = True
                logger.info(
                    "The server is still shutting_down the room. "
                    "Please wait...",
                )
                sleep(5)
                continue
            # purging
            if json_response["status"] == "purging":
                if not msglock_purging:
                    print(
                        "Status: Purging (purging the room and event data from"
                        " database)",
                    )
                msglock_purging = True
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


def handle_arguments(arg: Namespace) -> JsonDict:
    """Build the parameters used for the delroom request.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``

    Returns
    -------
    body : matrixctl.typehints.JsonDict
        The params.

    """
    if arg.force_purge and arg.no_purge:
        arg.no_purge = False

    body: JsonDict = {
        "block": arg.block,
        "purge": arg.no_purge,
        "force_purge": arg.force_purge,
    }
    if arg.new_room_admin is not None:
        body["new_room_user_id"] = arg.new_room_admin
        body["room_name"] = arg.new_room_name
        if arg.message is None:
            body["message"] = (
                f"{arg.room} has been shutdown due to content violations "
                "on this server. Please review our Terms of Service."
            )
        else:
            body["message"] = arg.message

    logger.debug("Body: %s", body)
    return body


# vim: set ft=python :
