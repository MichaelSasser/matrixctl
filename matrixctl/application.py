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
# PYTHON_ARGCOMPLETE_OK
import sys
import argparse
from logging import debug, warning

import coloredlogs
import argcomplete

from matrixctl import __version__
from .config_handler import Config
from .adduser import subparser_adduser
from .deluser import subparser_deluser
from .adduser_jitsi import subparser_adduser_jitsi
from .deluser_jitsi import subparser_deluser_jitsi
from .users import subparser_users
from .user import subparser_user
from .housekeeping import maintainance, restart, check
from .provisioning import deploy
from .updating import update


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

# API: https://github.com/matrix-org/synapse/blob/master/docs/admin_api/user_admin_api.rst


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enables debugging mode."
    )
    subparsers = parser.add_subparsers()

    subparser_adduser(subparsers)
    subparser_deluser(subparsers)
    subparser_adduser_jitsi(subparsers)
    subparser_deluser_jitsi(subparsers)
    subparser_users(subparsers)
    subparser_user(subparsers)

    ##########################################################################
    # update
    update_parser = subparsers.add_parser(
        "update", help="Updates the ansible repo"
    )
    update_parser.set_defaults(func=update)

    ##########################################################################
    # deploy
    deploy_parser = subparsers.add_parser(
        "deploy", help="Provision and deploy"
    )
    deploy_parser.set_defaults(func=deploy)

    ##########################################################################
    # start
    start_parser = subparsers.add_parser(
        "start", help="Starts all OCI containers"
    )
    start_parser.set_defaults(func=restart)  # Keep it "restart"

    ##########################################################################
    # restart
    restart_parser = subparsers.add_parser(
        "restart", help="Restarts all OCI containers (alias for start)"
    )
    restart_parser.set_defaults(func=restart)

    ##########################################################################
    # maintainance
    maintainance_parser = subparsers.add_parser(
        "maintainance", help="Run maintainance tasks"
    )
    maintainance_parser.set_defaults(func=maintainance)

    ##########################################################################
    # check
    check_parser = subparsers.add_parser(
        "check", help="Checks the OCI containers"
    )
    check_parser.set_defaults(func=check)

    ##########################################################################
    # Parsing
    argcomplete.autocomplete(parser)
    args: argparse.Namespace = parser.parse_args()

    coloredlogs.DEFAULT_LOG_FORMAT = (
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    coloredlogs.DEFAULT_LOG_LEVEL = 0 if args.debug else 21
    coloredlogs.install()

    config = Config()

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
        args.func(args, config)
        sys.exit()

    try:
        args.func(args, config)
    except AttributeError:
        parser.print_help()


# vim: set ft=python :
