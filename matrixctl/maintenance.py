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
from logging import debug

from .handlers.ansible import Ansible
from .handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_maintenance(subparsers: SubParsersAction) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "maintenance", help="Run maintenance tasks"
    )
    parser.set_defaults(func=maintenance)


def maintenance(_: Namespace) -> int:
    debug("maintenance")

    with TOML() as toml:
        with Ansible(toml.get(("SYNAPSE", "Path"))) as ansible:
            ansible.tags = (
                "run-postgres-vacuum",
                "start",
            )
            ansible.run_playbook()

    return 0


# vim: set ft=python :
