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
import json
import os
import subprocess
from logging import debug
from pathlib import Path
from typing import Iterable
from typing import List
from typing import Optional

from matrixctl.typing import JsonDict

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class Ansible:
    def __init__(
        self, playbook_path: Path, playbook: str = "setup.yml"
    ) -> None:
        assert isinstance(playbook_path, Path)
        assert isinstance(playbook, str)
        self.playbook_path: Path = playbook_path
        self.playbook: str = playbook
        self.__ansible_cfg_path: Optional[str] = None
        self.__cmd: dict = {  # Defaults are already in here
            "inventory": str(self.playbook_path / "inventory/hosts"),
        }

    def inventory_path(self, path):
        assert isinstance(path, Path)
        self.__cmd["inventory"]: str = str(path)

    def tags(self, tags: Iterable[str]):
        assert isinstance(tags, Iterable)
        self.__cmd["tags"]: str = ",".join(tags)  # e.g. tag1,tag2,...,tagn

    def extra_vars(self, extra_vars: JsonDict):
        assert isinstance(extra_vars, JsonDict)
        self.__cmd["extra_vars"]: str = json.dumps(extra_vars)

    def ansible_cfg_path(self, path):
        assert isinstance(path, str)
        self.__ansible_cfg_path = path

    inventory_path = property(fset=inventory_path)
    tags = property(fset=tags)
    extra_vars = property(fset=extra_vars)
    ansible_cfg_tags = property(fset=ansible_cfg_path)

    def run_playbook(self) -> None:
        # Build the command
        cmd: List[str] = ["ansible-playbook"]

        for k in self.__cmd:
            cmd.append(f"--{k}={self.__cmd[k]}")

        cmd.append(str(self.playbook_path / self.playbook))

        # Debug output of the command
        debug(f"Ansible command:           {cmd}")
        debug(f"Ansible assembled command: {' '.join(cmd)}")

        # Add ansible.cfg to ENV

        if self.__ansible_cfg_path is not None:
            os.environ["ANSIBLE_CONFIG"] = self.__ansible_cfg_path

        # Run command
        subprocess.run(cmd, check=True)

        # Delete ansible.cfg from ENV

        if self.__ansible_cfg_path is not None:
            del os.environ["ANSIBLE_CONFIG"]

    # def run_server_playbook(
    #     self,
    #     playbook_path: str,
    #     tags: Optional[str] = None,
    #     ansible_cfg_path: Optional[str] = None,
    # ) -> None:
    #     """This function runs your own playbook, if it is configured in the
    #     the MatrixCtl config file in section ``[SERVER]``.
    #
    #     This is useful, if you proision the server with your own Ansible
    #     playbook.
    #
    #     The output of the ``ansible-playbook`` program is using both
    #     ``stdout``
    #     and ``stderr``. For the user is no visual difference if this function
    #     executes the program (ansible-playbook) or if the user executes the
    #     program manuelly.
    #
    #     :param playbook_path:  The path to the playbook
    #     :param server_cfg_path:    The path to the ansible.cfg (optional,
    #                              default: ``None``)
    #     :param tags:      Additional tags (optional, default: ``None``)
    #     :return:                 None
    #     """
    #
    #     # Add ENV variable
    #
    #     if ansible_cfg_path is not None:
    #         os.environ["ANSIBLE_CONFIG"] = ansible_cfg_path
    #
    #     # Build command
    #     cmd: List[str] = ["ansible-playbook"]
    #
    #     if tags is not None:
    #         cmd.append(f"--tags={tags}")
    #
    #     cmd.append(playbook_path)
    #
    #     # Run command
    #     subprocess.run(cmd, check=True)
    #
    #     # Delete ENV variable
    #
    #     if ansible_cfg_path is not None:
    #         del os.environ["ANSIBLE_CONFIG"]
    #
    # def run_synapse_playbook(
    #     self, playbook_path: Path, arguments: Iterable[str]
    # ) -> None:
    #     """This function runs the ``spantaleev/matrix-docker-ansible-deploy``
    #     playbook, if it is configured in the the MatrixCtl config file in
    #     section ``[ANSIBLE]``.
    #
    #     The output of the ``ansible-playbook`` program is using both
    #     ``stdout``
    #     and ``stderr``. For the user is no visual difference if this function
    #     executes the program (ansible-playbook) or if the user executes the
    #     program manuelly.
    #
    #     :param ansible_path:  The path to the playbook
    #     :return:                 None
    #     """
    #     assert isinstance(arguments, (list, tuple))
    #
    #     if playbook_path is None:
    #         error(
    #             "To be able to use this function, you need to have "
    #             "the spantaleev/matrix-docker-ansible-deploy playbook "
    #             "configured in your MatrixCtl config file"
    #         )
    #         sys.exit(1)
    #
    #     # Build Command
    #     cmd: List[str] = [
    #         "ansible-playbook",
    #         "--inventory",
    #         f"{str(playbook_path)}/inventory/hosts",
    #         f"{str(playbook_path)}/setup.yml",
    #     ]
    #     cmd += list(arguments)
    #
    #     # Run command
    #     subprocess.run(cmd, check=True)

    def __enter__(self):
        """Makes it possible to be called with the ``with`` statement.
        This is currently not really needed, but unifis the way handlers are
        used.
        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Makes it possible to be called with the ``with`` statement.
        This is currently not really needed, but unifis the way handlers are
        used.
        """

        return


# vim: set ft=python :
