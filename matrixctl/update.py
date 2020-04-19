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
from __future__ import annotations

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction

from .handlers.git import Git
from .handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_update(subparsers: SubParsersAction) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "update", help="Updates the ansible repo"
    )
    parser.set_defaults(func=update)


def update(_: Namespace) -> int:
    with TOML() as toml:
        with Git(toml.get(("SYNAPSE", "Path"))) as git:
            git.pull()

    return 0


# vim: set ft=python :
