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
from logging import debug, error
from typing import Optional

import requests

from matrixctl import __version__
from .config_handler import Config

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class Api:
    def __init__(self, config: Config):
        self.config = config
        self.url = f"https://matrix.{self.config.api_domain}"
        self.session = requests.Session()

    def adduser(self, user: str, password: str, admin: bool = False):
        """Add a user to the matrix server."""
        path = f"/users/@{user}:{self.config.api_domain}"
        payload = {
            "password": password,
            "admin": admin,
        }
        response = self.send(path, payload=payload, method="PUT")

        if response.status_code not in (201, requests.codes.ok):
            error("The User was not added.")

    def deluser(self, user: str):
        """Add a user to the matrix server."""
        path = f"/deactivate/@{user}:{self.config.api_domain}"
        payload = {
            "erase": True,
        }
        response = self.send(
            path, payload=payload, method="POST", api_version=1
        )

        if response.status_code not in (201, requests.codes.ok):
            error("The User was not added.")

    def send(
        self,
        path: str,
        params: Optional[dict] = None,
        payload: Optional[dict] = None,
        method: str = "GET",
        api_version: int = 2,
        json_payload: bool = True,
    ):
        method = method.upper()
        assert method in {"GET", "POST", "PUT", "DELETE"}

        api_path = f"/_synapse/admin/v{api_version}"
        headers: dict = {
            "User-Agent": f"matrixctl{__version__}",
            "Authorization": f"Bearer {self.config.api_token}",
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


# if __name__ == "__main__":
#     from pprint import pprint  # noqa
#
#     r_path = "/users?guests=false"
#     r_params = {"limit": 3}
#     api = Api()
#     pprint(api.send(r_path, params=r_params))

# vim: set ft=python :
