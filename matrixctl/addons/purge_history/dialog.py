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

"""The purge-history command allows to purge historic events from the database.

Use this module to add the ``purge-histoy`` subcommand to ``matrixctl``.
"""

from __future__ import annotations

import logging
import sys
import time

from argparse import Namespace

from .timing import check_point_in_time

from matrixctl.password_helpers import ask_question


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def dialog_input(arg: Namespace) -> dict[str, str | int]:
    """Ask questions and sanitize them.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.

    Returns
    -------
    request_body : typing.Dict [str, str] or NoReturn
        Non-zero value indicates error code, or zero on success.

    """
    request_body: dict[str, str | int] = {}

    # Sanitizing input

    # check room_id (! = internal; # = local)
    if not (arg.room_id.startswith("!") or arg.room_id.startswith("#")):
        logger.critical("The room_id is incorrect. Please check it again.")
        sys.exit(1)

    # Delete local events; Q: Are you sure?
    if arg.local_events:
        if not arg.force:
            print(
                "You are about to delete *local* message events from the "
                "Database. As they may represent the only copy of this "
                "content in existence, you need to confirm this action.",
            )
            if not ask_question("Do you want to continue?"):
                sys.exit(0)
        request_body["delete_local_events"] = True

    # Delete all but the last message event; Q: Are you sure?
    if arg.event_or_timestamp is None:
        if not arg.force:
            print(
                "You are about to delete all message events except the last "
                "one.",
            )
            if not ask_question("Do you want to continue?"):
                sys.exit(0)
        request_body["purge_up_to_ts"] = int(round(time.time() * 1000))
    else:
        point_in_time: dict[str, str | int] | None = check_point_in_time(
            arg.event_or_timestamp,
        )

        if point_in_time is None:
            logger.critical(
                "The event/timestamp does not seem to be correct. "
                "Please check that argument again.",
            )
            sys.exit(1)
        request_body = {**request_body, **point_in_time}

    return request_body


# vim: set ft=python :
