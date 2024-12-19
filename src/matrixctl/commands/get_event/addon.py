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

"""Use this module to get an event from the Database."""

from __future__ import annotations

import json
import logging
import typing as t

from argparse import Namespace

from matrixctl.handlers.db import db_connect
from matrixctl.handlers.yaml import YAML
from matrixctl.sanitizers import sanitize_event_identifier


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Get an Event from the Server.

    It connects via paramiko to the server and runs the psql command provided
    by the synapse playbook to run a query on the Database.

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

    event_identifier: str | t.Literal[False] | None = (
        sanitize_event_identifier(arg.event_id)
    )
    if not event_identifier:
        return 1

    response: str | None = None
    with db_connect(yaml) as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT json FROM event_json WHERE event_id=(%s)",
            (event_identifier,),
        )
        response_ = cur.fetchone()
        if response_ is not None:
            response = response_[0]
    if response is not None:
        try:
            print(json.dumps(json.loads(response), indent=4))
        except json.decoder.JSONDecodeError:
            logger.exception("Unable to process the response data to JSON.")
            return 1
        except Exception:
            logger.exception(
                (
                    "Unable to process the response data to JSON."
                    "Response was None"
                ),
            )
            return 1
    return 0


# vim: set ft=python :
