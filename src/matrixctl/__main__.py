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

"""Use this module as entrypoint for the application."""

from __future__ import annotations

import argparse
import logging

from importlib import import_module
from pathlib import Path
from types import ModuleType

import coloredlogs

from matrixctl import __version__
from matrixctl import addon_manager
from matrixctl.handlers.yaml import YAML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

# API:
# https://element-hq.github.io/synapse/latest/admin_api/user_admin_api.html


logger = logging.getLogger(__name__)


def setup_parser() -> argparse.ArgumentParser:
    """Use this class to initialize the parser.

    Parameters
    ----------
    None

    Returns
    -------
    parser : argparse.ArgumentParser
        The parser object, which can be used to parse the arguments.

    """
    parser = argparse.ArgumentParser(
        description=(
            "MatrixCtl is a simple, but feature-rich tool to remotely "
            "control, manage, provision and deploy Matrix homeservers."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Thank you for using MatrixCtl!\n"
            "Check out the docs: https://matrixctl.rtfd.io\n"
            "Report bugs to: "
            "https://github.com/MichaelSasser/matrixctl/issues/new/choose"
        ),
    )

    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enables debugging mode.",
    )
    parser.add_argument(
        "-s",
        "--server",
        help='Select the server. (default: "default")',
    )
    parser.add_argument(
        "-c",
        "--config",
        help="A path to an alternative config file.",
    )
    return parser


def setup_logging(*, debug_mode: bool) -> None:
    """Use this function to setup logging for the application.

    Parameters
    ----------
    debug_mode : bool
        ``True`` sets the log level to ``DEBUG``, ``False`` sets the log level
        to ``INFO``.

    Returns
    -------
    None

    """
    # Default coloredlogs.DEFAULT_LOG_FORMAT:
    # %(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s

    coloredlogs.install(
        level="DEBUG" if debug_mode else "WARNING",
        fmt=(
            "%(asctime)s %(name)s:%(lineno)d [%(funcName)s] %(levelname)s "
            "%(message)s"
        ),
    )

    logger_httpx = logging.getLogger("hpack.hpack")
    logger_sshtunnel = logging.getLogger("sshtunnel")
    logger_httpx.setLevel(logging.INFO if debug_mode else logging.WARNING)
    logger_sshtunnel.disabled = not debug_mode


def main() -> int:
    """Use the ``main`` function as entrypoint to run the application.

    Parameters
    ----------
    None

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    addon_module = "matrixctl.commands"
    addon_dir: Path = Path(__file__).resolve().parent / "commands"

    # Setup Commands
    addon_manager.import_commands_from(str(addon_dir), addon_module, "parser")
    parser: argparse.ArgumentParser = addon_manager.setup(setup_parser)

    args: argparse.Namespace = parser.parse_args()

    setup_logging(debug_mode=args.debug)

    logger.debug("args: %s", args)

    yaml: YAML = YAML(
        None if args.config is None else (args.config,),
        args.server,
    )

    try:
        addon_module_import: str = f"{addon_module}.{args.addon}.addon"
    except AttributeError as e:
        if args.debug:
            logger.exception(
                "The parser of the addon which has been called did not have "
                'an arg "args.addon". If you did not enter an subcommand, '
                'e.g. "matrixctl -d" you can ignore this error.',
            )
            raise AttributeError(e) from e
        parser.print_help()
        return 1

    logger.debug("addon_module_import: %s", addon_module_import)
    addon: ModuleType = import_module(addon_module_import)

    if args.debug:
        logger.debug("Disabing help on AttributeError")  # may not be needed
        logger.warning(
            "In debugging mode help is disabled! If you don't use any "
            "attributes, the program will throw a AttributeError like: "
            "\"AttributeError: 'Namespace' object has no attribute 'func\".'"
            " This is perfectly normal and not a bug. If you want the help "
            'in debug mode, use the "--help" attribute.',
        )

        # Both should fail without catching the error
        return int(addon.addon(args, yaml))  # type: ignore # noqa: PGH003

    try:
        return int(addon.addon(args, yaml))  # type: ignore # noqa: PGH003
    except AttributeError:
        parser.print_help()

        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())

# vim: set ft=python :
