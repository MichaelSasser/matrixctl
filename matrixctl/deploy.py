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

import sys

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction
from logging import debug
from logging import error

from .handlers.ansible import Ansible
from .handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_deploy(subparsers: SubParsersAction) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "deploy", help="Provision and deploy"
    )
    parser.set_defaults(func=deploy)


def deploy(_: Namespace) -> int:
    debug("deploy")
    with TOML() as toml:
        if (
            toml.get(("ANSIBLE", "Path")) is None
            and toml.get(("SYNAPSE", "Path")) is None
        ):
            error(
                "To be able to use the deploy feature, you need to have "
                "At least your own Ansible playbook configuration in the "
                "MatrixCtl config file or the "
                "spantaleev/matrix-docker-ansible-deploy "
                "playbook"
            )
            sys.exit(1)

        if toml.get(("ANSIBLE", "Path")) is not None:
            with Ansible(toml.get(("ANSIBLE", "Path"))) as ansible:
                ansible.tags = toml.get(("ANSIBLE", "DeployTags"))
                ansible.ansible_cfg_path = toml.get(("ANSIBLE", "Cfg"))
                ansible.run_playbook()

        if toml.get(("SYNAPSE", "Path")) is not None:
            with Ansible(toml.get(("SYNAPSE", "Path"))) as ansible:
                ansible.tags = ("setup-all",)
                ansible.run_playbook()

        return 0


# vim: set ft=python :
