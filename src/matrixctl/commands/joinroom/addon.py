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

"""Use this module to add the ``joinroom`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from argparse import Namespace

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Join a user to an room.

    Notes
    -----
    - You can only modify the membership of local users.
    - The the token of server administrator used to authenticate against the
      homeserver must be in the room and must have permission to invite users.

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
    # sanitize
    arg.room = arg.room.strip()
    arg.user = arg.user.strip()

    if arg.room[0] not in {"!", "#"} or ":" not in arg.room:
        logger.error(
            "Make sure, to use the correct room identifier or alias e.g. "
            "!636q39766251:domain.tld or #myroom:domain.tld",
        )
    if not arg.user.startswith("@"):
        arg.user = f"@{arg.user}"

    if ":" not in arg.user:
        arg.user = f"{arg.user}:{yaml.get('server', 'api','domain')}"

    logger.debug("room = %s", arg.room)
    logger.debug("user = %s", arg.user)

    # request
    request_config: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path=f"/_synapse/admin/v1/join/{arg.room}",
        method="POST",
        json={"user_id": arg.user},
    )
    try:
        request(request_config)
    except InternalResponseError:
        logger.exception(
            "Unknown Error. The user was not joined to the room.",
        )

    return 0


# vim: set ft=python :
