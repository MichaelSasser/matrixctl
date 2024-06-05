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

"""Add the ``purge-remote-media`` subcommand to ``matrixctl``."""

from __future__ import annotations

import typing as t

from argparse import ArgumentParser
from argparse import _SubParsersAction

from matrixctl.addon_manager import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser
def subparser_purge_remote_media(subparsers: _SubParsersAction[t.Any]) -> None:
    """Create a subparser for the ``matrixctl purge-remote-media`` command.

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
        "purge-remote-media",
        help="Purge cached, remote media",
    )
    parser.add_argument(
        "timestamp",
        type=int,
        nargs="?",
        default=None,
        help=(
            "All cached media that was last accessed before this timestamp"
            " (UNIX epoch) will be removed"
        ),
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="No questions asked",
    )
    parser.add_argument(
        "-j",
        "--to-json",
        action="store_true",
        help="Output the data as JSON",
    )
    parser.set_defaults(addon="purge_remote_media")


# vim: set ft=python :
