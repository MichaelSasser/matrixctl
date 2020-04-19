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
from types import TracebackType
from typing import NamedTuple
from typing import Optional
from typing import Type

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

    def __init__(self, address: str):
        self.address: str = address
        self.client: SSHClient = SSHClient()
        self.client.load_system_host_keys()
        self.__connect()

    def __connect(self) -> None:
        """Connect to the SSH server."""
        self.client.connect(self.address)

    @staticmethod
    def __str_from(f: ChannelFile) -> Optional[str]:
        try:
            return str(f.read().decode("utf-8").strip())
        except OSError:
            return None

    def run_cmd(self, cmd: str) -> SSHResponse:
        debug(f'SSH Command: "{cmd}"')

        response: SSHResponse = SSHResponse(
            *[self.__str_from(s) for s in self.client.exec_command(cmd)]
        )

        debug(f'SSH Response: "{response}"')

        return response

    def __enter__(self) -> SSH:
        """Connect to the SSH server with the "with" statement."""

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Close the SSH connection."""
        self.client.close()

    def __del__(self) -> None:
        """Close the connection to the SSH."""
        self.client.close()


# vim: set ft=python :
