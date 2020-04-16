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
import os
import subprocess
import sys
from logging import debug
from logging import error
from pathlib import Path
from typing import Iterable
from typing import List
from typing import Optional

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def ansible_server(
    server_playbook: str,
    server_tags: Optional[str] = None,
    server_config: Optional[str] = None,
) -> None:
    """This function runs your own playbook, if it is configured in the
    the MatrixCtl config file in section ``[SERVER]``.

    This is useful, if you proision the server with your own Ansible
    playbook.

    The output of the ``ansible-playbook`` program is using both ``stdout``
    and ``stderr``. For the user is no visual difference if this function
    executes the program (ansible-playbook) or if the user executes the
    program manuelly.

    :param server_playbook:  The path to the playbook
    :param server_config:    The path to the ansible.cfg (optional, default:
                             ``None``)
    :param server_tags:      Additional tags (optional, default: ``None``)
    :return:                 None
    """

    # Add ENV variable

    if server_config is not None:
        os.environ["ANSIBLE_CONFIG"] = server_config

    # Build command
    cmd: List[str] = [
        "ansible-playbook",
        server_playbook,
    ]

    if server_tags is not None:
        cmd.append(f"--tags={server_tags}")

    # Run command
    subprocess.run(cmd, check=True)

    # Delete ENV variable

    if server_config is not None:
        del os.environ["ANSIBLE_CONFIG"]


def ansible_synapse(arguments: Iterable[str], ansible_path: Path) -> None:
    """This function runs the ``spantaleev/matrix-docker-ansible-deploy``
    playbook, if it is configured in the the MatrixCtl config file in section
    ``[ANSIBLE]``.

    The output of the ``ansible-playbook`` program is using both ``stdout``
    and ``stderr``. For the user is no visual difference if this function
    executes the program (ansible-playbook) or if the user executes the
    program manuelly.

    :param ansible_path:  The path to the playbook
    :return:                 None
    """
    assert isinstance(arguments, (list, tuple))

    if ansible_path is None:
        error(
            "To be able to use this function, you need to have "
            "the spantaleev/matrix-docker-ansible-deploy playbook "
            "configured in your MatrixCtl config file"
        )
        sys.exit(1)

    # Build Command
    cmd: List[str] = [
        "ansible-playbook",
        "-i",
        f"{str(ansible_path)}/inventory/hosts",
        f"{str(ansible_path)}/setup.yml",
    ]
    cmd += list(arguments)
    debug(f"ansible_synapse: {cmd=}")
    debug(f"ansible_synapse assembled: {' '.join(cmd)}")

    # Run command
    subprocess.run(cmd, check=True)


# vim: set ft=python :
