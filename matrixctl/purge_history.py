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

"""The purge-history command allows to purge historic events from the database.

Use this module to add the ``purge-histoy`` subcommand to ``matrixctl``.
"""

from __future__ import annotations

import logging

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction
from datetime import datetime
from time import sleep
from typing import Dict
from typing import Optional
from typing import Union

from .errors import InternalResponseError
from .handlers.api import API
from .handlers.toml import TOML
from .password_helpers import ask_question
from .typing import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def subparser_purge_history(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl purge-history`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "purge-history", help="Purge historic events from the DB"
    )
    parser.add_argument(
        "-l",
        "--local-events",
        action="store_true",
        help="Delete local message events as well",
    )
    parser.add_argument(
        "room_id",
        type=str,
        help="The Room to purge historic message events in",
    )
    parser.add_argument(
        "event_or_timestamp",
        type=str,
        nargs="?",
        default=None,
        help=(
            "An event or timestamp (UNIX epoch, in milliseconds) as point in "
            "the room to purge up to"
        ),
    )
    parser.set_defaults(func=purge_history)


def check_point_in_time(
    event_or_timestamp: str,
) -> Optional[Dict[str, Union[str, int]]]:
    """Check the the type of the point in time and set the correct body.

    Parameters
    ----------
    event_or_timestamp : str
        The event_id or timestamp (UNIX epoch, in milliseconds).

    Returns
    -------
    request_body: Dict [str, str or int]
        A dict, which can be merged with the request_body dict.

    """
    try:
        dt = datetime.fromtimestamp(float(event_or_timestamp) / 1000)
        logger.debug(f"Delete until {dt=}")
        return {"purge_up_to_ts": int(event_or_timestamp)}
    except (OverflowError, OSError, ValueError):
        if event_or_timestamp.startswith("$"):
            return {"purge_up_to_event_id": event_or_timestamp}
    return None


def handle_purge_status(toml: TOML, purge_id: str) -> int:
    """Check the status pf the purge history request.

    Parameters
    ----------
    toml : matrixctl.handlers.toml.TOML
        The configuration file handler.
    purge_id: str
        The purge id from a purge history request.

    Returns
    -------
    response: matrixctl.typing.JsonDict, optional
        The response as dict, containing the status.

    """
    api: API = API(toml.get("API", "Domain"), toml.get("API", "Token"))
    api.url.path = f"purge_history_status/{purge_id}"
    api.url.api_version = "v1"
    api.method = "GET"

    while True:

        try:
            response: JsonDict = api.request().json()
        except InternalResponseError:
            logger.critical(
                "The purge history request was successful but the status "
                "request failed. You just have to wait a bit."
                "If that happens the next time, pleas hand in a bug report."
            )
            return 1
        # return response

        if response is not None:
            logger.debug(f"{response=}")
            if response["status"] == "complete":
                print("Done...")
                return 0
            if response["status"] == "failed":
                logger.critical(
                    "The server returned, that the purge aproach failed."
                )
                break
            if response["status"] == "active":
                logger.info(
                    "The server is still purging historic message content. "
                    "Please wait..."
                )
                sleep(2)  # wait 2 seconds before try again
                continue
        break
    return 0


def purge_history(arg: Namespace) -> int:
    """Purge historic message events from the Database.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    request_body: Dict[str, Union[str, int]] = {}

    # Sanitizing input

    # check room_id (! = internal; # = local)
    if not (arg.room_id.startswith("!") or arg.room_id.startswith("#")):
        logger.critical("The room_id is incorrect. Pleas check it again.")
        return 1

    # Delete local events; Q: Are you sure?
    if arg.local_events:
        print(
            "You are about to delete *local* message events from the "
            "Database. As they may represent the only copies of this content "
            "in existence, you need to conform this action."
        )
        if not ask_question("Do you want to continue?"):
            return 0
        request_body["delete_local_events"] = True

    # Delete all but the last message event; Q: Are you sure?
    if arg.event_or_timestamp is None:
        print("You are about to delete all mesage events except the last one.")
        if not ask_question("Do you want to continue?"):
            return 0
    else:
        point_in_time: Optional[
            Dict[str, Union[str, int]]
        ] = check_point_in_time(arg.event_or_timestamp)

        if point_in_time is None:
            logger.critical(
                "The event/timestamp does not seem to be correct. "
                "Please check that argument again."
            )
            return 1
        request_body = {**request_body, **point_in_time}

    # # Ask at least one time.
    # if not ask_question(
    #     "You are about to delete message events. Do you want to continue?"
    # ):
    #     return 0

    # Worker

    toml: TOML = TOML()

    api: API = API(toml.get("API", "Domain"), toml.get("API", "Token"))
    api.url.path = f"purge_history/{arg.room_id}"
    api.url.api_version = "v1"
    api.method = "POST"

    try:
        response: JsonDict = api.request(request_body).json()
    except InternalResponseError:
        logger.critical(
            "Something went wrong with the request. Please check your data "
            "again."
        )
        return 1

    logger.debug(f"{response=}")
    return handle_purge_status(toml, response["purge_id"])
    ###################
    # while True:
    #     status_response: Optional[JsonDict] = get_purge_status(
    #         toml, response["purge_id"]
    #     )
    #
    #     if status_response is not None:
    #         debug(f"{status_response=}")
    #         if status_response["status"] == "complete":
    #             print("Done...")
    #             return 0
    #         if status_response["status"] == "failed":
    #             fatal("The server returned, that the purge aproach failed.")
    #             break
    #         if status_response["status"] == "active":
    #             info(
    #                 "The server is still purging historic message content. "
    #                 "Please wait..."
    #             )
    #             sleep(2)  # wait 2 seconds before try again
    #             continue
    #     break
    #
    # return 1


# vim: set ft=python :
