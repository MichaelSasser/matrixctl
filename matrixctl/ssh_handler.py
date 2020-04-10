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
from typing import NamedTuple, Optional
from logging import debug, error

from paramiko import SSHClient
from paramiko.channel import ChannelFile

from .config_handler import Config


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class SSHResponse(NamedTuple):
    stdin: Optional[str]
    stdout: Optional[str]
    stderr: Optional[str]


class Ssh:

    JID_EXT: str = "matrix-jitsi-web"

    def __init__(self, cfg: Config, address: str = None):
        self.config: Config = cfg

        if address is None:
            address = f"matrix.{self.config.api_domain}"
        self.address: str = address
        self.client: SSHClient = SSHClient()
        self.client.load_system_host_keys()
        self.connect()

    def connect(self):
        """Connects to the SSH server"""
        self.client.connect(self.address)

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

    def adduser(self, user: str, password: str):
        """Add a user to the jitsi server."""
        # register: undocumented, means: "user@JID_EXT passwd" as stdin
        # without asking for the password. (replaces adduser)
        cmd: str = f'sudo docker exec matrix-jitsi-prosody prosodyctl --config /config/prosody.cfg.lua register "{user}" {self.__class__.JID_EXT} "{password}"'

        res = self.run_cmd(cmd)

        if res.stderr.startswith("bash: 7: command not found"):
            error(
                "BUG: It's likely that you had previously installed Jitsi "
                "without auth/guest support. Please look into the "
                "configuring-playbook-jitsi.md in "
                "matrix-docker-ansible-deploy/docs. Read the paragraph "
                "about rebuilding your Jitsi installation."
            )
            sys.exit(1)

        return res

    def deluser(self, user: str):
        """Delete a user from the jitsi server."""
        cmd: str = f'sudo docker exec matrix-jitsi-prosody prosodyctl --config /config/prosody.cfg.lua deluser "{user}@{self.__class__.JID_EXT}"'

        return self.run_cmd(cmd)


# vim: set ft=python :
