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
from typing import Iterable, List
from .config_handler import Config

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def ansible_server(cfg: Config) -> None:
    if cfg.server_play is not None:

        # Add ENV variable

        if cfg.server_cfg is not None:
            os.environ["ANSIBLE_CONFIG"] = cfg.server_cfg

        # Build command
        cmd: List[str] = [
            "ansible-playbook",
            cfg.server_play,
        ]

        if cfg.server_tags is not None:
            cmd.append(f"--tags={cfg.server_tags}")

        # Run command
        subprocess.run(cmd, check=True)

        # Delete ENV variable

        if cfg.server_cfg is not None:
            del os.environ["ANSIBLE_CONFIG"]


def ansible_synapse(arguments: Iterable[str], cfg: Config) -> None:
    assert isinstance(arguments, (list, tuple))

    # Build Command
    cmd: List[str] = [
        "ansible-playbook",
        "-i",
        f"{str(cfg.ansible_path)}/inventory/hosts",
        f"{str(cfg.ansible_path)}/setup.yml",
    ]
    cmd += list(arguments)

    # Run command
    subprocess.run(cmd, check=True)


# vim: set ft=python :
