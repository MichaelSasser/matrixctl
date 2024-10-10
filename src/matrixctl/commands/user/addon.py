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

"""Use this module to add the ``user`` subcommand to ``matrixctl``."""

from __future__ import annotations

import json
import logging

from argparse import Namespace

from .to_table import to_table

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.yaml import YAML
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(arg: Namespace, yaml: YAML) -> int:
    """List information about an registered user.

    It uses the admin API to get a python dictionary with the information.
    The ``generate_user_tables`` function makes the information human readable.

    Examples
    --------
    .. code-block:: console

       $ matrixctl user dwight
       User:
       +----------------------------+--------------------------------------+
       | Name                       | dwight                               |
       | Password Hash              | $2b$12$9DUNderm1ffL1NincPap3RC       |
       |                            | ompaNY1725.slOUghAvEnu5cranT0n       |
       | Guest                      | False                                |
       | Admin                      | True                                 |
       | Consent Version            |                                      |
       | Consent Server Notice Sent |                                      |
       | Appservice Id              |                                      |
       | Creation Ts                | 2020-04-14 13:04:21                  |
       | User Type                  |                                      |
       | Deactivated                | False                                |
       | Displayname                | Dwight Schrute                       |
       | Avatar Url                 | mxc://dunder-mifflin.com/sCr4        |
       |                            | nt0nsr4ng13rW45Cr33d                 |
       +----------------------------+--------------------------------------+

       Threepid:
       +--------------+-----------------------------------+
       | Medium       | email                             |
       | Address      | dwight_schrute@dunder-mifflin.com |
       | Validated At | 2020-04-14 15:30:21.123000        |
       | Added At     | 2020-04-14 15:29:19.100000        |
       +--------------+-----------------------------------+

    If the user does not exist, the return looks like:

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
    len_domain = len(yaml.get("server", "api", "domain")) + 1
    user_id = f"@{arg.user}:{yaml.get('server', 'api', 'domain')}"
    req: RequestBuilder = RequestBuilder(
        token=yaml.get("server", "api", "token"),
        domain=yaml.get("server", "api", "domain"),
        path=f"/_synapse/admin/v2/users/{user_id}",
    )

    try:
        user_dict: JsonDict = request(req).json()
    except InternalResponseError:
        logger.critical("Could not receive the user information")

        return 1

    if arg.to_json:
        print(json.dumps(user_dict, indent=4))
    else:
        for line in to_table(user_dict, len_domain):
            print(line)

    return 0


# vim: set ft=python :
