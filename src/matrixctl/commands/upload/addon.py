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

"""Use this module to add the ``upload`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from argparse import Namespace
from mimetypes import MimeTypes
from pathlib import Path

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Upload a file or image to the matrix instance.

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
    file_path: Path = Path(arg.file).absolute()
    logger.debug("upload file_path: %s", file_path)
    mime_types: MimeTypes = MimeTypes()
    file_type: str = str(mime_types.guess_type(file_path.name)[0])
    logger.debug("upload file_type: %s", file_type)
    try:
        with file_path.open("rb") as fp:
            file: bytes = fp.read()
    except FileNotFoundError:
        print("No such file found. Please check your filepath.")
        return 1

    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path="/_matrix/media/r0/upload/",
        method="POST",
        headers={"Content-Type": file_type},
        content=file,
    )
    try:
        response: JsonDict = request(req).json()
    except InternalResponseError:
        logger.exception("The file was not uploaded.")
        return 1
    try:
        print("Content URI: ", response["content_uri"])
    except KeyError as e:
        msg: str = (
            f"Upload was successful, but no content_uri was found. {response}"
        )
        raise InternalResponseError(msg) from e
    return 0


# vim: set ft=python :
