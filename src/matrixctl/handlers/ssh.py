# matrixctl
# Copyright (c) 2020-2023  Michael Sasser <Michael@MichaelSasser.org>
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

import logging
import shlex
import typing as t

from getpass import getuser
from types import TracebackType

from paramiko import AutoAddPolicy
from paramiko import SSHClient
from paramiko.channel import ChannelFile  # noqa: TC002


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


class SSHResponse(t.NamedTuple):
    """Store the response of a SSH command as response."""

    stdin: str | None
    stdout: str | None
    stderr: str | None


class SSH:
    """Run and evaluate commands on the host machine of your synapse server."""

    __slots__ = ("__client", "address", "port", "user")

    def __init__(
        self: SSH,
        address: str,
        user: str | None = None,
        port: int = 22,
    ) -> None:
        self.address: str = address
        self.port: int = port
        self.user: str = getuser() if user is None else user
        self.__client: SSHClient = SSHClient()
        self.__client.load_system_host_keys()
        self.__client.set_missing_host_key_policy(AutoAddPolicy())
        self.__connect()

    def __connect(self: SSH) -> None:
        """Connect to the SSH server.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self.__client.connect(self.address, self.port, self.user)
        logger.debug("SSH connected")

    def __disconnect(self: SSH) -> None:
        """Disconnect from the SSH server.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self.__client.close()
        logger.debug("SSH disconnected")

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

    def run_cmd(self: SSH, cmd: str) -> SSHResponse:
        """Run a command on the host machine and receive a response.

        Parameters
        ----------
        cmd : str
            The command to run.
        tty : bool
            Request a pseudo-terminal from the server (default: ``False``)

        Returns
        -------
        response : matrixctl.handlers.ssh.SSHResponse
            Receive ``stdin``, ``stdout`` and ``stderr`` as response.

        """
        logger.debug("SSH Command: %s", cmd)

        response: SSHResponse = SSHResponse(
            *[
                self.__str_from(s)
                # false positive
                # skipcq BAN-B601
                for s in self.__client.exec_command(shlex.quote(cmd))
            ],
        )

        logger.debug("SSH Response: %s", response)

        return response

    def __enter__(self: SSH) -> SSH:  # noqa: PYI034
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
        self: SSH,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
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
        logger.debug(
            "SSH __exit__: exc_type = %s, exc_val = %s, exc_tb = %s",
            exc_type,
            exc_val,
            exc_tb,
        )
        self.__disconnect()

    def __del__(self: SSH) -> None:
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
