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

"""Use this module to add the ``maintenance`` subcommand to ``matrixctl``."""

from __future__ import annotations

import typing as t

from argparse import ArgumentParser
from argparse import _SubParsersAction

from matrixctl.addon_manager import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser
def subparser_maintenance(subparsers: _SubParsersAction[t.Any]) -> None:
    """Create a subparser for the ``matrixctl maintenance`` command.

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
        "maintenance",
        help="Run maintenance tasks",
        description="Perform various maintenance tasks.",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="Show a list of all available tasks",
    )
    parser.add_argument(
        "tasks",
        nargs="*",
        help="Maintenance tasks to run (overrides configuration)",
    )
    parser.set_defaults(addon="maintenance")


# vim: set ft=python :
