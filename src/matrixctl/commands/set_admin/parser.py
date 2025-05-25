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

"""Use this module to add the ``set-admin`` subcommand to ``matrixctl``."""

from __future__ import annotations

import typing as t

from argparse import ArgumentParser
from argparse import _SubParsersAction

from matrixctl.command import SubCommand
from matrixctl.command import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser(SubCommand.USER)
def subparser_set_admin(
    subparsers: _SubParsersAction[t.Any],
    common_parser: ArgumentParser,
) -> None:
    """Create a subparser for the ``matrixctl set-admin`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction of typing.Any
        The object which is returned by
        ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "set-admin",
        help="Give a user administrator privileges or remove them from them",
        parents=[common_parser],
    )
    parser.add_argument(
        "user",
        help="The localpart of the user to promote/demote",
    )
    parser.add_argument(
        "admin",
        choices=["promote", "demote"],
        help="Promote or demote a user",
    )
    parser.set_defaults(addon="set_admin")


# vim: set ft=python :
