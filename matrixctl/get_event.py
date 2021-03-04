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

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction
from pprint import pprint

from .handlers.ssh import SSH
from .handlers.ssh import SSHResponse
from .handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

JID_EXT: str = "matrix-jitsi-web"


def subparser_get_event(subparsers: SubParsersAction) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "get-event", help="get an event from the db"
    )
    parser.add_argument("event_id", help="The event-id")
    parser.set_defaults(func=get_event)


def get_event(arg: Namespace) -> int:
    """Get an Event from the Server.

    It runs ``ask_password()``
    first. If ``ask_password()`` returns ``None`` it generates a password
    with ``gen_password()``. Then it gives the user a overview of the
    username, password and if the new user should be generated as admin
    (if you added the ``--admin`` argument). Next, it asks a question,
    if the entered values are correct with the ``ask_question`` function.

    If the ``ask_question`` function returns True, it continues. If not, it
    starts from the beginning.

    It runs the ``adduser`` method of the ``Ssh`` class.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :return:          None
    """

    toml: TOML = TOML()
    address = (
        toml.get("SSH", "Address")
        if toml.get("SSH", "Address")
        else f"matrix.{toml.get('API', 'Domain')}"
    )
    query: str = (
        f"SELECT json FROM event_json WHERE event_id='${arg.event_id}'"
    )
    cmd: str = "/usr/local/bin/matrix-postgres-cli"
    table: str = "synapse"

    command: str = f"sudo {cmd} -d {table} -c '{query}'"
    # cmd: str = (
    #     "sudo echo "
    #     f'"SELECT "json" FROM event_json WHERE event_id=\'\\${arg.event_id}\'"'
    # )

    with SSH(address, toml.get("SSH", "User"), toml.get("SSH", "Port")) as ssh:
        response: SSHResponse = ssh.run_cmd(command, tty=True)

    if not response.stderr:
        print(response.stdout)
    else:
        print(
            "An error occured during the query. Are you sure, you used the "
            "correct event_id?"
        )
        return 1

    return 0


# vim: set ft=python :
