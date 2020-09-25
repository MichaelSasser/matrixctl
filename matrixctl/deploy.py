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
    parser.add_argument(
        "-s",
        "--synapse",
        action="store_true",
        help="Deploy only the synapse playbook",
    )
    parser.add_argument(
        "-a",
        "--ansible",
        action="store_true",
        help="Deploy only your own playbook",
    )
    parser.set_defaults(func=deploy)


def deploy(arg: Namespace) -> int:
    """Deploy the ansible playbook.

    **Contol logic**

    a = ta  (TOML Ansible)
    b = ts  (TOML SYNAPSE)
    A = arg.ansible
    B = arg.synapse

    Empirical:
    Ansible = a/A/B + aA
    Synapse = b/A/B + bB
    Error = /a/b + /aA + /bB

    Optimized (factored SOP):

    Ansible = a(/A/B + A)
    Synapse = b(/A/B + B)
    Error = /b(B + /a) + /aA
    """
    debug("deploy")
    with TOML() as toml:
        # make them shorter
        ta: bool = toml.get(("ANSIBLE", "Path"), True) is not None
        ts: bool = toml.get(("SYNAPSE", "Path"), True) is not None

        if not ts and (arg.synapse or not ta) or not ta and arg.ansible:
            error(
                "To be able to use the deploy feature, you need to have "
                "At least your own Ansible playbook configuration in the "
                "MatrixCtl config file or the "
                "spantaleev/matrix-docker-ansible-deploy "
                "playbook"
            )
            sys.exit(1)

        if ta and (not arg.ansible and not arg.synape or arg.ansible):
            with Ansible(toml.get(("ANSIBLE", "Path"))) as ansible:
                ansible.tags = toml.get(("ANSIBLE", "DeployTags"))
                ansible.ansible_cfg_path = toml.get(("ANSIBLE", "Cfg"))
                ansible.run_playbook()

        if ts and (not arg.ansible and not arg.synapse or arg.synapse):
            with Ansible(toml.get(("SYNAPSE", "Path"))) as ansible:
                ansible.tags = ("setup-all",)
                ansible.run_playbook()

        return 0


# vim: set ft=python :
