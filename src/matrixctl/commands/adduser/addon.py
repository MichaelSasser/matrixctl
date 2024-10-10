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

"""Use this module to add the ``adduser`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from argparse import Namespace

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.ansible import ansible_run
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.password_helpers import create_user


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Add a User to the synapse instance.

    It runs ``ask_password()`` first. If ``ask_password()`` returns ``None``
    it generates a password with ``gen_password()``. Then it gives the user
    a overview of the username, password and if the new user should be
    generated as admin (if you added the ``--admin`` argument). Next, it asks
    a question, if the entered values are correct with the ``ask_question``
    function.

    If the ``ask_question`` function returns True, it continues. If not, it
    starts from the beginning.

    Depending on the ``--ansible`` switch it runs the ``adduser`` command
    via ansible or the API

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
    passwd: str = create_user(arg.user, arg.admin)

    if arg.ansible:
        ansible_run(
            playbook=yaml.get("server", "ansible", "playbook"),
            tags="register-user",
            extra_vars={
                "username": arg.user,
                "password": passwd,
                "admin": "yes" if arg.admin else "no",
            },
        )
        return 0

    user_id = f"@{arg.user}:{yaml.get('server', 'api','domain')}"
    req: RequestBuilder = RequestBuilder(
        domain=yaml.get("server", "api", "domain"),
        token=yaml.get("server", "api", "token"),
        path=f"/_synapse/admin/v2/users/{user_id}",
        json={"password": passwd, "admin": arg.admin},
        method="PUT",
    )
    try:
        request(req)
    except InternalResponseError:
        logger.exception("The User was not added.")

    return 0


# vim: set ft=python :
