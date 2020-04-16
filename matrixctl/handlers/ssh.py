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
from typing import NamedTuple, Optional
from logging import debug

from paramiko import SSHClient
from paramiko.channel import ChannelFile


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class SSHResponse(NamedTuple):
    stdin: Optional[str]
    stdout: Optional[str]
    stderr: Optional[str]


class SSH:
    __slots__ = ("address", "client")

    def __init__(self, address: str = None):
        self.address: str = address
        self.client: SSHClient = SSHClient()
        self.client.load_system_host_keys()
        self.__connect()

    def __connect(self):
        """Connects to the SSH server"""
        self.client.connect(self.address)

    @staticmethod
    def __str_from(f: ChannelFile) -> Optional[str]:
        try:
            return f.read().decode("utf-8").strip()
        except OSError:
            return None

    def run_cmd(self, cmd: str):
        debug(f'SSH Command: "{cmd}"')

        response = SSHResponse(
            *[self.__str_from(s) for s in self.client.exec_command(cmd)]
        )

        debug(f'SSH Response: "{response}"')

        return response

    def __enter__(self):
        """Connects to the SSH server with the "with" command"""

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the connection to the SSH after the namespace of the
        "with" command ends."""
        self.client.close()

    def __del__(self):
        """Clos the connection to the SSH"""
        self.client.close()


# vim: set ft=python :
