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

import json
import os
import subprocess

from logging import debug
from pathlib import Path
from types import TracebackType
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Type
from typing import Union

from matrixctl.typing import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


# ToDO: __slots__
class Ansible:
    def __init__(
        self, path: Union[Path, str], playbook: str = "setup.yml"
    ) -> None:
        self.path: Path = Path(path)

        assert isinstance(playbook, str)

        self.playbook: str = playbook
        self.__ansible_cfg_path: Optional[str] = None
        self.__cmd: Dict[str, str] = {  # Defaults are already in here
            "inventory": str(self.path / "inventory/hosts"),
        }

    def _inventory_path(self, path: Path) -> None:
        assert isinstance(path, Path)
        self.__cmd["inventory"] = str(path)

    def _tags(self, tags: Iterable[str]) -> None:
        assert isinstance(tags, Iterable)
        self.__cmd["tags"] = ",".join(tags)  # e.g. tag1,tag2,...,tagn

    def _extra_vars(self, extra_vars: JsonDict) -> None:
        self.__cmd["extra-vars"] = json.dumps(extra_vars).replace(" ", "")

    def _ansible_cfg_path(self, path: Path) -> None:
        assert isinstance(path, str)
        self.__ansible_cfg_path = path

    inventory_path = property(fset=_inventory_path)
    tags = property(fset=_tags)
    extra_vars = property(fset=_extra_vars)
    ansible_cfg_path = property(fset=_ansible_cfg_path)

    def run_playbook(self) -> None:
        # Build the command
        cmd: List[str] = ["ansible-playbook"]

        for k in self.__cmd:
            cmd.append(f"--{k}={self.__cmd[k]}")

        cmd.append(str(self.path / self.playbook))

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

    def __enter__(self) -> Ansible:
        """Use the class with the ``with`` statement`` statement.

        This is currently not really needed, but unifies the way handlers are
        used.
        """

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Use the class with the ``with`` statement`` statement.

        This is currently not really needed, but unifies the way handlers are
        used.
        """

        return


# vim: set ft=python :
