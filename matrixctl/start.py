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

from logging import debug

from .handlers.ansible import Ansible

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_start(subparsers):
    start_parser = subparsers.add_parser(
        "start", help="Starts all OCI containers"
    )
    start_parser.set_defaults(func=start)


def subparser_restart(subparsers):
    restart_parser = subparsers.add_parser(
        "restart", help="Restarts all OCI containers (alias for start)"
    )
    restart_parser.set_defaults(func=start)  # Keep it "start"


def start(_, cfg):
    debug("start")

    with Ansible(cfg.synapse_path) as ansible:
        ansible.tags = ("start",)
        ansible.run_playbook()


# vim: set ft=python :
