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

"""Add the ``delete-local_media`` subcommand to ``matrixctl``."""

from __future__ import annotations

from argparse import ArgumentParser
from argparse import _SubParsersAction

from matrixctl.addon_manager import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser
def subparser_delete_local_media(subparsers: _SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl delete-local_media`` command.

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
        "delete-local-media",
        help=("delete local media"),
    )
    parser.add_argument(
        "timestamp",
        type=int,
        nargs="?",
        default=None,
        help=(
            "A timestamp (UNIX epoch, in milliseconds). All cached media that "
            "was last accessed before this timestamp will be removed"
        ),
    )
    parser.add_argument(
        "--no-keep-profiles",
        action="store_false",
        help=(
            "also delete files that are still used in image data "
            "(e.g user profile, room avatar)"
        ),
    )
    parser.add_argument(
        "-g",
        "--greater-than",
        type=int,
        default=0,
        help=(
            "Size of the media in bytes. Files that are larger will be "
            "deleted. default: 0"
        ),
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="No questions asked",
    )
    parser.set_defaults(addon="delete_local_media")


# vim: set ft=python :