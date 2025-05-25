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

"""Use this module to dynamically create a commands structure."""

from __future__ import annotations

import argparse
import logging
import typing as t

from collections.abc import Callable
from enum import Enum
from enum import auto
from importlib import import_module
from pkgutil import iter_modules


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)

# Leave them here, as long as they are not needed elsewhere
# skipcq: PYL-W0212  # noqa: ERA001
# pyright: reportPrivateUsage=false
SubParsersAction = argparse._SubParsersAction  # noqa: SLF001
SubParserType = Callable[
    [SubParsersAction, argparse.ArgumentParser],  # type: ignore # noqa: PGH003
    None,
]
ParserSetupType = Callable[
    [], tuple[argparse.ArgumentParser, argparse.ArgumentParser]
]

# global


# StrEnum was 3.11
class SubCommand(Enum):
    """Use to enumerate possible subcommands for the command-line interface.

    Each member represents a distinct subcommand that can be invoked by the
    user.

    """

    ROOM = auto()
    USER = auto()
    MEDIA = auto()
    SERVER = auto()
    MOD = auto()
    SELF = auto()

    def get_help(self) -> str:
        """Get a help string for the subcommand."""
        match self:
            case SubCommand.ROOM:
                return "Manage rooms."
            case SubCommand.USER:
                return "Manage users."
            case SubCommand.MEDIA:
                return "Manage media files on the server."
            case SubCommand.SERVER:
                return "Manage the homeserver instance."
            case SubCommand.MOD:
                return "Moderation commands for rooms and users."
            case SubCommand.SELF:
                return "Manage MatrixCtl."

    @staticmethod
    def generate_commands() -> dict[SubCommand, list[SubParserType]]:
        """Generate a dictionary of subcommands with empty lists."""
        return {c: [] for c in SubCommand}

    def __str__(self) -> str:
        """Return the string representation of the subcommand."""
        match self:
            case SubCommand.ROOM:
                return "room"
            case SubCommand.USER:
                return "user"
            case SubCommand.MEDIA:
                return "media"
            case SubCommand.SERVER:
                return "server"
            case SubCommand.MOD:
                return "mod"
            case SubCommand.SELF:
                return "self"


# Global commands dictionary
commands: dict[SubCommand, list[SubParserType]] = (
    SubCommand.generate_commands()
)


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


def subparser(
    subcommand: SubCommand,
) -> t.Callable[[SubParserType], SubParserType]:
    """Decorate subparsers with, to add them to (global) commands on import.

    Parameters
    ----------
    fn : matrixctl.addon_manager.SubParserType
        The supparser to be wrapped.

    subcommand : matrixctl.addon_manager.SubCommand
        The subcommand (or category) to which the subparser belongs.

    ..Note:
        Nothing will be imported, when the subparser is not in (global)
        commands. To add the subparse to commands you need to decorate the
        subparsers with ``matrixctl.addon_manager.subparser``

    Returns
    -------
    decorated_func : matrixctl.addon_manager.SubParserType
        The same subparser which was used as argument. (Without any changes)

    """

    def subparser_inner(fn: SubParserType) -> SubParserType:
        """Inner function to register the subparser."""

        if fn not in commands[subcommand]:
            commands[subcommand].append(fn)
        return fn

    return subparser_inner


def create_error_handler(
    parser: argparse.ArgumentParser,
) -> t.Callable[[str], None]:
    """Create a custom error handler for each subparser to display its help.

    Creates a custom error handler for an argparse subparser that prints
    the parser's help message and exits with status code 2 when called.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        The subparser to handle errors for.

    Returns
    -------
    handler : Callable[[str], None]
        The error handler function.

    """

    def handler(_: str) -> None:
        """Use this as a custom error handler for the subparser."""

        parser.print_help()
        parser.exit(2)

    return handler


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
            '"Command.import_commands_from()"?',
        )

    parser: argparse.ArgumentParser
    common_parser: argparse.ArgumentParser
    parser, common_parser = func()
    if len(commands) > 0:
        command_base: SubParsersAction[t.Any] = parser.add_subparsers(
            title="Categoties",
            description=(
                "Please select a category to see the available commands."
            ),
            metavar="Category",
        )

        for subcommand in SubCommand:
            # Create a subparser for each subcommand
            nested_parser = command_base.add_parser(
                str(subcommand), help=subcommand.get_help()
            )
            if subcommand in commands:
                subcommand_base = nested_parser.add_subparsers(
                    title="Commands",
                    description="Available Commands.",
                    metavar="Command",
                )
                subcommand_base.required = True
                nested_parser.set_defaults()
                for subparser_ in commands[subcommand]:
                    subparser_(subcommand_base, common_parser)

            # Hook in our custom error handler
            nested_parser.error = create_error_handler(nested_parser)

    return parser
