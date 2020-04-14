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
import sys
from logging import debug, error
from .ansible_handler import ansible_synapse, ansible_server

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def deploy(_, cfg):
    debug(f"deploy")

    if cfg.server_play is None and cfg.ansible_path is None:
        error(
            "To be able to use the deploy feature, you need to have "
            "At least your own Ansible playbook configuration in the "
            "MatrixCtl config file or the "
            "spantaleev/matrix-docker-ansible-deploy "
            "playbook"
        )
        sys.exit(1)

    if cfg.server_play is not None:
        ansible_server(cfg.server_play, cfg.server_cfg, cfg.server_tags)

    if cfg.ansible_path is not None:
        ansible_synapse(["--tags=setup-all"], cfg.ansible_path)


# vim: set ft=python :
