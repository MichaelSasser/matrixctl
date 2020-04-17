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
from logging import debug, error

from .handlers.ansible import Ansible

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_deploy(subparsers):
    deploy_parser = subparsers.add_parser(
        "deploy", help="Provision and deploy"
    )
    deploy_parser.set_defaults(func=deploy)


def deploy(_, cfg):
    debug("deploy")

    if cfg.my_playbook is None and cfg.synapse_path is None:
        error(
            "To be able to use the deploy feature, you need to have "
            "At least your own Ansible playbook configuration in the "
            "MatrixCtl config file or the "
            "spantaleev/matrix-docker-ansible-deploy "
            "playbook"
        )
        sys.exit(1)

    if cfg.my_playbook is not None:

        print(cfg.my_playbook, type(cfg.my_playbook))
        with Ansible(cfg.my_playbook) as ansible:
            ansible.tags = (cfg.server_tags,)  # ToDo: make list
            ansible.ansible_cfg_path = cfg.server_cfg
            ansible.run_playbook()

    if cfg.synapse_path is not None:
        with Ansible(cfg.synapse_path) as ansible:
            ansible.tags = ("setup-all",)
            ansible.run_playbook()


# vim: set ft=python :
