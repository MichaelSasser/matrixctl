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

"""Use this module to add a ``deluser-jitsi`` subcommand to ``matrixctl``."""

from __future__ import annotations

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction

from .handlers.ssh import SSH
from .handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


JID_EXT: str = "matrix-jitsi-web"


def subparser_deluser_jitsi(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl deluser-jitsi`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by
        ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "deluser-jitsi", help="Deletes a jitsi user"
    )
    parser.add_argument("user", help="The jitsi username to delete")
    parser.set_defaults(func=deluser_jitsi)


def deluser_jitsi(arg: Namespace) -> int:
    """Delete a user from the jitsi instance.

    It uses the ``Ssh`` class from the ``ssh_handler``.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    toml: TOML = TOML()
    address = (
        toml.get("SSH", "Address")
        if toml.get("SSH", "Address")
        else f"matrix.{toml.get('API','Domain')}"
    )
    with SSH(address, toml.get("SSH", "User"), toml.get("SSH", "Port")) as ssh:
        cmd: str = (
            "sudo docker exec matrix-jitsi-prosody prosodyctl "
            "--config /config/prosody.cfg.lua deluser "
            f'"{arg.user}@{JID_EXT}"'
        )

        ssh.run_cmd(cmd)

    return 0


# vim: set ft=python :
