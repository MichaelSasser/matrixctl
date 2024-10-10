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

"""Use this module as addon manager."""

from __future__ import annotations

import argparse
import logging
import typing as t

from collections.abc import Callable
from importlib import import_module
from pkgutil import iter_modules


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)

# Leave them here, as long as they are not needed elsewhere
# skipcq: PYL-W0212  # noqa: ERA001
# pyright: reportPrivateUsage=false
SubParsersAction = argparse._SubParsersAction  # noqa: SLF001
SubParserType = Callable[[SubParsersAction], None]  # type: ignore # noqa: PGH003
ParserSetupType = Callable[[], argparse.ArgumentParser]

# global
commands: list[SubParserType] = []


def import_commands_from(
    addon_directory: str,
    addon_module: str,
    parser_name: str,
) -> None:
    """Import commands in (global) commands.

    Parameters
    ----------
    addon_directory : str
        The absolute path as string to the addon directory.
    addon_module : str
        The import path (with dots ``.`` not slashes ``/``) to the commands
        from project root e.g. "matrixctl.commands".
    parser_name : str
        The name of the module the subparser is in.
    ..Note:
        The nothing will be imported, when the subparser is not in (global)
        commands. To add the subparse to commands you need to decorate the
        subparsers with ``matrixctl.addon_manager.subparser``

    Returns
    -------
    none : None
        The function always returns ``None``.

    """
    logger.debug("package dir set to %s", addon_directory)
    logger.debug("addon_module set to %s", addon_module)
    for _, module_name, _ in iter_modules(
        [addon_directory],
        f"{addon_module}.",
    ):
        parser = f"{module_name}.{parser_name}"
        logger.debug("Found module: %s", parser)
        module = import_module(parser)
        logger.debug("Imported: %s", module)


def subparser(func: SubParserType) -> SubParserType:
    """Decorate subparsers with, to add them to (global) commands on import.

    Parameters
    ----------
    func : matrixctl.addon_manager.SubParserType
        A subparser.
    ..Note:
        The nothing will be imported, when the subparser is not in (global)
        commands. To add the subparse to commands you need to decorate the
        subparsers with ``matrixctl.addon_manager.subparser``

    Returns
    -------
    decorated_func : matrixctl.addon_manager.SubParserType
        The same subparser which was used as argument. (Without any changes)

    """
    if func not in commands:
        commands.append(func)
    return func


def setup(func: ParserSetupType) -> argparse.ArgumentParser:
    """Add subparsers to the (main) parser.

    Parameters
    ----------
    func : matrixctl.addon_manager.ParserSetupType
        A callback to the main parser.

    Returns
    -------
    parser : argparse.ArgumentParser
        The parser which includes all subparsers.

    """

    if len(commands) == 0:
        logger.error(
            "The Argparse Addon Manager was not able to find any commands. "
            "Have you imported the commands with "
            '"AddonManager.import_commands_from()"?',
        )

    parser: argparse.ArgumentParser = func()
    if len(commands) > 0:
        subparsers: SubParsersAction[t.Any] = parser.add_subparsers(
            title="Commands",
            description=(
                "The following are commands, you can use to accomplish "
                "various tasks."
            ),
            metavar="Command",
        )
        for subparser_ in commands:
            subparser_(subparsers)
    return parser
