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

"""Use this module to add the ``users`` subcommand to ``matrixctl``."""

from __future__ import annotations

import typing as t

from argparse import ArgumentParser
from argparse import _SubParsersAction

from matrixctl.command import SubCommand
from matrixctl.command import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser(SubCommand.USER)
def subparser_users(
    subparsers: _SubParsersAction[t.Any],
    common_parser: ArgumentParser,
) -> None:
    """Create a subparser for the ``matrixctl users`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction of typing.Any
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "users",
        help="Lists all users registerd to the homeserver",
        parents=[common_parser],
    )
    parser.add_argument(
        "limit",
        type=int,
        default=-1,
        nargs="?",
        help="Limit the number of users shown",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Show all users",
    )
    parser.add_argument(
        "-g",
        "--with-guests",
        action="store_true",
        help="Also include guest accounts",
    )
    parser.add_argument(
        "-D",
        "--with-deactivated",
        action="store_true",
        help="Also include deactivated accounts",
    )
    parser.add_argument(
        "-j",
        "--to-json",
        action="store_true",
        help="Change the output format to JSON",
    )
    parser.set_defaults(addon="users")


# vim: set ft=python :
