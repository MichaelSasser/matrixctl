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
from .api_handler import Api
from .housekeeping import maintainance
from .updating import update
from .account import adduser, deluser
from .provisioning import deploy


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

    # adduser
    adduser_parser = subparsers.add_parser("adduser", help="Add a user")
    adduser_parser.add_argument("user", help="The Username of the new user")
    adduser_parser.add_argument(
        "-p",
        "--passwd",
        help="The password of the new user. (If you don't enter a password, "
        "you will be asked later.)",
    )
    adduser_parser.add_argument(
        "-a", "--admin", action="store_true", help="Create as admin user"
    )
    adduser_parser.add_argument(
        "--ansible", action="store_true", help="Use ansible insted of the api"
    )
    adduser_parser.set_defaults(func=adduser)

    # deluser
    deluser_parser = subparsers.add_parser("deluser", help="Deletes a user")
    deluser_parser.add_argument("user", help="The Username to delete")
    deluser_parser.set_defaults(func=deluser)

    # deploy
    deploy_parser = subparsers.add_parser(
        "deploy", help="Provision and deploy"
    )
    deploy_parser.set_defaults(func=deploy)

    # deploy
    update_parser = subparsers.add_parser(
        "update", help="Updates the ansible repo"
    )
    update_parser.set_defaults(func=update)

    # maintainance
    maintainance_parser = subparsers.add_parser(
        "maintainance", help="Run Maintainance tasks"
    )
    maintainance_parser.set_defaults(func=maintainance)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    coloredlogs.DEFAULT_LOG_FORMAT = (
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    coloredlogs.DEFAULT_LOG_LEVEL = 0 if args.debug else 20
    coloredlogs.install()

    config = Config()
    api = Api(config)

    if args.debug:
        debug("Disabing help on AttributeError")
        warning(
            "In debugging mode help is disabled! If you don't use any "
            "attibutes, the program will throw a AttributeError like: "
            "\"AttributeError: 'Namespace' object has no attribute 'func\".'"
            " This is perfectly normal and not a bug. If you want the help "
            'in debug mode, use the "--help" attribute.'
        )
        args.func(args, config, api)
        sys.exit()

    try:
        args.func(args, config, api)
    except AttributeError:
        parser.print_help()


# vim: set ft=python :
