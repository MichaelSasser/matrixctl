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


"""Use this module to add the ``adduser-jitsi`` subcommand to ``matrixctl``."""

from __future__ import annotations

from argparse import Namespace

from matrixctl.handlers.ssh import SSH
from matrixctl.handlers.yaml import YAML
from matrixctl.password_helpers import create_user


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


JID_EXT: str = "matrix-jitsi-web"


def addon(arg: Namespace, yaml: YAML) -> int:
    """Add a User to the jitsi instance.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.
    yaml : matrixctl.handlers.yaml.YAML
        The configuration file handler.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    address = (
        yaml.get("server", "ssh", "address")
        if yaml.get("server", "ssh", "address")
        else f"matrix.{yaml.get('server', 'api', 'domain')}"
    )
    with SSH(
        address,
        yaml.get("server", "ssh", "user"),
        yaml.get("server", "ssh", "port"),
    ) as ssh:

        passwd: str = create_user(arg.user)

        cmd: str = (
            "sudo docker exec matrix-jitsi-prosody prosodyctl "
            f"--config /config/prosody.cfg.lua register "
            f'"{arg.user}" {JID_EXT} "{passwd}"'
        )

        ssh.run_cmd(cmd)

        return 0


# vim: set ft=python :
