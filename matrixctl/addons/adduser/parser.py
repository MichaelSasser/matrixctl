# matrixctl
# Copyright (c) 2020-2021  Michael Sasser <Michael@MichaelSasser.org>
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

"""Use this module to add the ``adduser`` subcommand to ``matrixctl``."""

from __future__ import annotations

from argparse import ArgumentParser
from argparse import _SubParsersAction

from matrixctl.addon_manager import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser
def subparser_adduser(subparsers: _SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl adduser`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by
        ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "adduser", help="Add a new matrix user"
    )
    parser.add_argument("user", help="The Username of the new user")
    parser.add_argument(
        "-a", "--admin", action="store_true", help="Create as admin user"
    )
    parser.add_argument(
        "--ansible", action="store_true", help="Use ansible insted of the api"
    )

    parser.set_defaults(addon="adduser")


# vim: set ft=python :
