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

"""Use this module to add the ``(re)start`` subcommand to ``matrixctl``."""

from __future__ import annotations

import typing as t

from argparse import ArgumentParser
from argparse import _SubParsersAction

from matrixctl.command import SubCommand
from matrixctl.command import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser(SubCommand.SERVER)
def subparser_start(
    subparsers: _SubParsersAction[t.Any],
    common_parser: ArgumentParser,
) -> None:
    """Create a subparser for the ``matrixctl start`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction of typing.Any
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "start",
        help="(Re)Start the OCI containers",
        parents=[common_parser],
    )
    parser.set_defaults(addon="start")


@subparser(SubCommand.SERVER)
def subparser_restart(
    subparsers: _SubParsersAction[t.Any],
    common_parser: ArgumentParser,
) -> None:
    """Create a subparser for the ``matrixctl restart`` command.

    Notes
    -----
    This is a alias for ``matrixctl start``

    See Also
    --------
    matrixctl.start.subparser_start : Subparser for ``matrixctl start``.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction or typing.Any
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "restart",
        help="(Re)Start the OCI containers (alias for start)",
        parents=[common_parser],
    )
    parser.set_defaults(addon="start")  # Keep it "start"


# vim: set ft=python :
