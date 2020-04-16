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
import json
import sys
from logging import debug
from logging import error
from logging import fatal
from typing import Optional

import requests

from .typing import JsonDict
from matrixctl import __version__

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class Api:
    """Handles the connection to the Representational State Transfer (REST)
    API of synapse and communication.
    """

    def __init__(self, api_domain: str, api_token: str) -> None:
        """Initializes the Api class and checks, if the parameter
        are there.

        :param api_domain:  The API domain (e.g. "domain.tld")
        :param api_token:   The access token of an admin
        :return:            ``None``
        """

        if api_domain is None or api_token is None:
            assert isinstance(api_domain, str)
            assert isinstance(api_token, str)

            fatal(
                "Please check your config file: [API] must have valid "
                "Domain and Token entries"
            )
            sys.exit(1)

        self.token: str = api_token
        self.domain: str = api_domain
        self.url = f"https://matrix.{self.domain}"
        self.session = requests.Session()

    def __enter__(self):
        """Makes it possible to be called with the ``ẁith`` statement.
        This is currently not really needed, but gives a good representation
        of the lifetime of this object.
        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Makes it possible to be called with the ``ẁith`` statement.
        This is currently not really needed, but gives a good representation
        of the lifetime of this object.
        """

        return

    def adduser(self, user: str, password: str, admin: bool = False) -> None:
        """Add a user to the matrix instance.

        :param user:      The user of the user to create
        :param password:  The password of the user
        :param admin:     ``True``, if the user should be created as
                          administrator, ``False`` if the user should not be
                          created as administrator
        :return:          ``None``
        """
        path = f"/users/@{user}:{self.domain}"
        payload = {
            "password": password,
            "admin": admin,
        }
        response = self.send(path, payload=payload, method="PUT")

        if response.status_code not in (201, 200):
            error("The User was not added.")

    def deluser(self, user: str):
        """Deletes a user from the matrix instance.

        :param user:      The user of the user to create
        :return:          ``None``
        """
        path = f"/deactivate/@{user}:{self.domain}"
        payload = {
            "erase": True,
        }
        response = self.send(
            path, payload=payload, method="POST", api_version=1
        )

        if response.status_code not in (201, 200):
            error("The User was not added.")

    def users(self, from_user: int = 0, show_guests: bool = False) -> JsonDict:
        """Gets a list of users and optional guests from the matrix instance.
        This method can download only 100 entries at once. To download another
        100 entries (99..199) you need to set the ``from_user`` argument to
        100.

        **Example**

        >>> api = Api(domain, tokenr)
        >>> api.users(0)
        # Users 0..99
        >>> api.users(100)
        # Users 100..199
        >>> api.users(200)
        # Users 200..299

        :param from_user:    The number of the user to begin with.
                             (default: 0)
        :param show_guests:  ``True`` to show guests, ``False`` to don't
                             (default: ``False``)
        :return:             A json dict with the requestet users
        """
        path = f"/users"
        params = {
            "from": from_user,
            "guests": "true" if show_guests else "false",
        }
        response = self.send(path, method="GET", params=params)

        if response.status_code not in (201, 200):
            error("The request was not successful.")

        return response.json()

    def user(self, user: str) -> JsonDict:
        """Get detailed information about a user.

        :param user:  The username
        :return:      A json dict of the requestes user
        """
        path = f"/users/{user}"
        response = self.send(path, method="GET")

        if response.status_code not in (201, 200):
            error("The request was not successful.")

        return response.json()

    def send(
        self,
        path: str,
        params: Optional[dict] = None,
        payload: Optional[dict] = None,
        method: str = "GET",
        api_version: int = 2,
        json_payload: bool = True,
    ) -> requests.Response:
        """Sends a request to the synapse api with the help of the
        ``requests`` module.

        :param path:          The path of the request
        :param params:        Params of the request
        :param payload:       The payload of the request
        :param method:        The response method: ``GET``, ``POST``,
                              ``PUT``, ``DELETE`` of the request
        :param api_version:   The version of the api of the request
        :param json_payload:  ``True`` if the request and the response should
                              be in the json format.
        :return:              Returns the response
        """
        method = method.upper()
        assert method in {"GET", "POST", "PUT", "DELETE"}

        api_path = f"/_synapse/admin/v{api_version}"
        headers: dict = {
            "User-Agent": f"matrixctl{__version__}",
            "Authorization": f"Bearer {self.token}",
        }

        if json_payload:
            headers["Content-Type"] = "application/json"

        endpoint = self.url + api_path + path

        if (
            headers["Content-Type"] == "application/json"
            and payload is not None
        ):
            payload = json.dumps(payload)

        debug(f"{endpoint=}")
        debug(f"{headers=}")
        debug(f"{params=}")
        debug(f"{payload=}")

        response = self.session.request(
            method, endpoint, headers=headers, data=payload, params=params
        )

        debug(f"{response.json()=}")

        return response


# vim: set ft=python :
