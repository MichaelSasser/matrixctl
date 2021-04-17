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

"""Use this module as entrypoint for the application."""

from __future__ import annotations

import argparse

from argparse import _SubParsersAction
from logging import debug
from logging import warning
from typing import Callable
from typing import List

import coloredlogs

from matrixctl import __version__
from matrixctl.adduser import subparser_adduser
from matrixctl.adduser_jitsi import subparser_adduser_jitsi
from matrixctl.check import subparser_check
from matrixctl.delroom import subparser_delroom
from matrixctl.deluser import subparser_deluser
from matrixctl.deluser_jitsi import subparser_deluser_jitsi
from matrixctl.deploy import subparser_deploy
from matrixctl.maintenance import subparser_maintenance
from matrixctl.rooms import subparser_rooms
from matrixctl.server_notice import subparser_server_notice
from matrixctl.start import subparser_restart
from matrixctl.start import subparser_start
from matrixctl.update import subparser_update
from matrixctl.upload import subparser_upload
from matrixctl.user import subparser_user
from matrixctl.users import subparser_users
from matrixctl.version import subparser_version


# Subparsers


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

# API: https://github.com/matrix-org/synapse/blob/master/docs/admin_api/
#              user_admin_api.rst


def setup_parser() -> argparse.ArgumentParser:
    """Use this class to initialize the parser and the subparsers.

    Parameters
    ----------
    None

    Returns
    -------
    parser : argparse.ArgumentParser
        The parser object, which can be used to parse the arguments.

    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enables debugging mode."
    )
    subparsers: _SubParsersAction = parser.add_subparsers()

    # Subparsers
    subparsers_tuple: List[Callable[[_SubParsersAction], None]] = [
        subparser_adduser,
        subparser_deluser,
        subparser_adduser_jitsi,
        subparser_deluser_jitsi,
        subparser_user,
        subparser_users,
        subparser_rooms,
        subparser_delroom,
        subparser_update,
        subparser_upload,
        subparser_deploy,
        subparser_server_notice,
        subparser_start,
        subparser_restart,  # alias for start
        subparser_maintenance,
        subparser_check,
        subparser_version,
    ]

    for subparser in subparsers_tuple:
        subparser(subparsers)

    return parser


def setup_logging(debug_mode: bool) -> None:
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
    coloredlogs.DEFAULT_LOG_FORMAT = (
        "%(asctime)s [%(module)s:%(lineno)d (%(funcName)s)] - %(levelname)s "
        "- %(message)s"
    )
    coloredlogs.DEFAULT_LOG_LEVEL = 0 if debug_mode else 21
    coloredlogs.install()


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
    parser = setup_parser()

    args: argparse.Namespace = parser.parse_args()

    setup_logging(args.debug)

    debug(f"{args=}")

    if args.debug:
        debug("Disabing help on AttributeError")
        warning(
            "In debugging mode help is disabled! If you don't use any "
            "attibutes, the program will throw a AttributeError like: "
            "\"AttributeError: 'Namespace' object has no attribute 'func\".'"
            " This is perfectly normal and not a bug. If you want the help "
            'in debug mode, use the "--help" attribute.'
        )

        return int(args.func(args))

    try:
        return int(args.func(args))
    except AttributeError:
        parser.print_help()

        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())

# vim: set ft=python :
