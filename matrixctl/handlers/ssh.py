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

"""Run and evaluate commands on the host machine of your synapse server."""

from __future__ import annotations

from getpass import getuser
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

    """Store the response of a SSH command as response."""

    stdin: Optional[str]
    stdout: Optional[str]
    stderr: Optional[str]


class SSH:

    """Run and evaluate commands on the host machine of your synapse server."""

    __slots__ = ("address", "__client", "user", "port")

    def __init__(
        self, address: str, user: Optional[str] = None, port: int = 22
    ) -> None:
        self.address: str = address
        self.port: int = port
        self.user: str = getuser() if user is None else user
        self.__client: SSHClient = SSHClient()
        self.__client.load_system_host_keys()
        self.__connect()

    def __connect(self) -> None:
        """Connect to the SSH server.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self.__client.connect(self.address, self.port, self.user)
        debug("SSH connected")

    def __disconnect(self) -> None:
        """Disconnect from the SSH server.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self.__client.close()
        debug("SSH disconnected")

    @staticmethod
    def __str_from(f: ChannelFile) -> str | None:
        """Convert a ChannelFile to str.

        Parameters
        ----------
        f : paramiko.channel.ChannelFile
            ``stdin``, ``stdout`` or ``stderr`` as ChannelFile.

        Returns
        -------
        response_str : str, optional
            ``stdin``, ``stdout`` or ``stderr`` as str.

        """
        try:
            return str(f.read().decode("utf-8").strip())
        except OSError:
            return None

    def run_cmd(self, cmd: str) -> SSHResponse:
        """Run a command on the host machine and receive a response.

        Parameters
        ----------
        cmd : str
            The command to run.

        Returns
        -------
        response : matrixctl.handlers.ssh.SSHResponse
            Receive ``stdin``, ``stdout`` and ``stderr`` as response.

        """
        debug(f'SSH Command: "{cmd}"')

        response: SSHResponse = SSHResponse(
            # skipcq: BAN-B601
            *[self.__str_from(s) for s in self.__client.exec_command(cmd)]
        )

        debug(f'SSH Response: "{response}"')

        return response

    def __enter__(self) -> SSH:
        """Connect to the SSH server with the "with" statement.

        Parameters
        ----------
        None

        Returns
        -------
        ssh_instance : matrixctl.handlers.ssh.SSH
            The object itself.

        """

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Close the SSH connection.

        Parameters
        ----------
        exc_type : types.Type [BaseException], optional
            (Unused)
        exc_val : BaseException, optional
            (Unused)
        exc_tb : types.TracebackType, optional
            (Unused)

        Returns
        -------
        None

        """
        debug(f"SSH __exit__: {exc_type=}, {exc_val=}, {exc_tb=}")
        self.__disconnect()

    def __del__(self) -> None:
        """Close the connection to the SSH.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self.__disconnect()


# vim: set ft=python :
