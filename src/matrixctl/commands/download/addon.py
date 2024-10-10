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

"""Use this module to add the ``download`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from argparse import Namespace
from pathlib import Path

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import streamed_download
from matrixctl.handlers.yaml import YAML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Download a file or image from the matrix instance.

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
    mxc: str = arg.mxc.strip()

    # TODO: Make this into a proper sanitizer. Therefore ignoring warnings.
    if not str(mxc).startswith("mxc://"):
        logger.error("The URI is not a valid matrix media URI.")
        return 1
    mxc_parts = mxc.removeprefix("mxc://").split("/")

    if len(mxc_parts) != 2:  # noqa: PLR2004
        logger.error("The URI is not a valid matrix media URI.")
        return 1
    homeserver, media_id = mxc_parts

    file_path: Path = Path(arg.file).absolute()
    logger.debug("Download file_path: %s", file_path)

    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path=f"/_matrix/client/v1/media/download/{homeserver}/{media_id}",
        method="GET",
        params={"allow_redirect": "true"},
    )
    # https://matrix.michaelsasser.org/_matrix/media/v3/download/matrix.org/rFzCZiffizZGTyWXWONCVjXw?allow_redirect=true

    try:
        streamed_download(req, file_path)
    except InternalResponseError:
        logger.exception("The file was not downloaded.")
        return 1
    except FileExistsError as err:
        if hasattr(err, "__repr__"):
            logger.error(repr(err))  # noqa: TRY400
        else:
            logger.error("The file already exists.")  # noqa: TRY400
        return 1
    return 0


# vim: set ft=python :
