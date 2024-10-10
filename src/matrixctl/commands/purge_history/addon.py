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

from argparse import Namespace
from contextlib import suppress

from .dialog import dialog_input
from .handler import handle_purge_status

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Purge historic message events from the Database.

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
    arg.room_id = arg.room_id.strip()

    request_body: dict[str, str | int] = dialog_input(arg)

    logger.debug("request_body: %s", request_body)

    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path=f"/_synapse/admin/v1/purge_history/{arg.room_id.strip()}",
        method="POST",
        json=request_body,
        timeout=10,
    )

    try:
        response: JsonDict = request(req).json()
    except InternalResponseError as e:
        with suppress(KeyError):
            if e.payload["errcode"] == "M_UNKNOWN":
                logger.critical(e.payload["error"])
                return 1
        logger.critical(
            "Something went wrong with the request. Please check your data "
            "again.",
        )
        return 1

    logger.debug("response: %s", response)
    return handle_purge_status(yaml, response["purge_id"])


# vim: set ft=python :
