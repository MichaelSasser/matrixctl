#!/usr/bin/env python
# matrixctl
# Copyright (c) 2020  Michael Sasser <Michael@MichaelSasser.org>
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

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction
from logging import debug
from logging import error
from mimetypes import MimeTypes
from pathlib import Path

from .errors import InternalResponseError
from .handlers.api import API
from .handlers.toml import TOML
from .typing import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_upload(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl upload`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "upload", help="Upload a file."
    )
    parser.add_argument("file", help="The path to a file or image to upload")
    parser.set_defaults(func=upload)


def upload(arg: Namespace) -> int:
    """Upload a file or image to the matix instance.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    file_path: Path = Path(arg.file).absolute()
    debug(f"upload: {file_path=}")
    mime_types: MimeTypes = MimeTypes()
    file_type: str = str(mime_types.guess_type(file_path.name)[0])
    debug(f"upload: {file_type=}")
    try:
        with file_path.open("rb") as fp:
            file: bytes = fp.read()
    except FileNotFoundError:
        print("No such file found. Please check your filepath.")
        return 1

    toml: TOML = TOML()
    api: API = API(toml.get("API", "Domain"), toml.get("API", "Token"))
    try:
        api.url.api_path = "_matrix/media"
        api.url.path = "upload/"
        api.url.api_version = "r0"
        api.method = "POST"
        api.json_format = False
        api.headers = {"Content-Type": file_type}
        response: JsonDict = api.request(file).json()
    except InternalResponseError:
        error("The file was not uploaded.")
        return 1
    try:
        print("Content URI: ", response["content_uri"])
    except KeyError as e:
        raise InternalResponseError(
            "Upload was successful, but no content_uri was found.", response
        ) from e
    return 0


# vim: set ft=python :
