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

"""Use this module to add the ``version`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from argparse import Namespace

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(_: Namespace, yaml: YAML) -> int:
    """Get the version of the Synapse instance.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.
        (Unused in this function)
    yaml : matrixctl.handlers.yaml.YAML
        The configuration file handler.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path="/_synapse/admin/v1/server_version",
    )
    try:
        response: JsonDict = request(req).json()
    except InternalResponseError:
        logger.critical("Could not get the server sersion.")

        return 1
    logger.debug("response: %s", response)
    try:
        print(f"Server Version: {response['server_version']}")
    except KeyError:
        logger.exception(
            "MatrixCtl was not able to read the server version.",
        )

    # DEPRECATED
    # TODO: Remove this feature
    try:
        print(f"Python Version: {response['python_version']}")
    except KeyError:
        logger.warning(
            "MatrixCtl was not able to read the Python version used by "
            "Synapse. In newer Synapse versions, this field is missing "
            "and this warning can be ignored.",
        )

    return 0


# vim: set ft=python :
