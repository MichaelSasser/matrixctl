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

"""Use this module as addon manager."""

from __future__ import annotations

import argparse
import logging

from functools import wraps
from importlib import import_module
from pkgutil import iter_modules
from typing import Callable


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)

# Leave them here, as long as they are not needed elsewhere
SubParserType = Callable[[argparse._SubParsersAction], None]
ParserSetupType = Callable[[], argparse.ArgumentParser]

# global
addons: list[SubParserType] = []


def import_addons_from(
    addon_directory: str, addon_module: str, subparser_name: str
):
    logger.debug(f"package dir set to {addon_directory}")
    logger.debug(f"addon_module set to {addon_module}")
    for (_, module_name, _) in iter_modules(
        [addon_directory], f"{addon_module}."
    ):
        subparser = f"{module_name}.{subparser_name}"
        logger.debug(f"Found module: {subparser}")
        module = import_module(subparser)
        logger.debug(f"Imported: {module}")


def subparser(func: SubParserType) -> SubParserType:
    if func not in addons:
        addons.append(func)

    # maybe return func?
    @wraps(func)
    def wrapper(parser: argparse._SubParsersAction) -> None:
        func(parser)

    return wrapper


def setup(func: ParserSetupType) -> argparse.ArgumentParser:

    if len(addons) == 0:
        logger.error(
            "The Argparse Addon Manager was not able to find any addons. "
            "Have you imported the addons with "
            '"AddonManager.import_addons_from()"?'
        )

    parser: argparse.ArgumentParser = func()
    if len(addons) > 0:
        subparsers: argparse._SubParsersAction = parser.add_subparsers()
        for subparser in addons:
            subparser(subparsers)
    return parser
