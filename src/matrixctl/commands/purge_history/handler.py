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

from time import sleep

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def handle_purge_status(yaml: YAML, purge_id: str) -> int:
    """Check the status of the purge history request.

    Parameters
    ----------
    yaml : matrixctl.handlers.yaml.YAML
        The configuration file handler.
    purge_id: str
        The purge id from a purge history request.

    Returns
    -------
    response: matrixctl.typehints.JsonDict, optional
        The response as dict, containing the status.

    """
    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path=f"/_synapse/admin/v1/purge_history_status/{purge_id}",
        method="GET",
        timeout=1200.0,
    )

    while True:
        sleep(1)
        try:
            response: JsonDict = request(req).json()
        except InternalResponseError:
            logger.critical(
                "The purge history request was successful but the status "
                "request failed. You just have to wait a bit."
                "If that happens the next time, please hand in a bug report.",
            )
            return 1

        if response is not None:
            logger.debug("response: %s", response)
            if response["status"] == "complete":
                print("Done...")
                return 0
            if response["status"] == "failed":
                logger.critical(
                    "The server returned, that the purge approach failed.",
                )
                break
            if response["status"] == "active":
                logger.info(
                    "The server is still purging historic message content. "
                    "Please wait...",
                )
                sleep(5)
                continue
        break
    return 0


# vim: set ft=python :
