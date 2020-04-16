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
from logging import debug
from typing import Iterable
from typing import Tuple
from urllib.parse import urlparse

import requests

from matrixctl import __version__
from matrixctl.errors import InternalResponseError


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class UrlBuilder:
    __slots__ = (
        "__scheme",
        "__subdomain",
        "__domain",
        "__api_path",
        "__api_version",
        "__path",
    )

    def __init__(self, default_domain: str) -> None:
        self.__scheme: str = "https"
        self.__subdomain: str = "matrix"
        self.__domain: str = default_domain
        self.__api_path: str = "_synapse/admin"
        self.__api_version: str = "v2"
        self.__path: str = ""

    def scheme(self, scheme: str) -> None:
        assert isinstance(scheme, str)
        self.__scheme = scheme

    def domain(self, domain: str) -> None:
        assert isinstance(domain, str)
        self.__domain = domain

    def subdomain(self, subdomain: str) -> None:
        assert isinstance(subdomain, str)
        self.__subdomain = subdomain

    def api_path(self, api_path: str) -> None:
        assert isinstance(api_path, str)
        self.__api_path = api_path

    def api_version(self, api_version: str) -> None:
        assert isinstance(api_version, str)
        self.__api_version = api_version

    def path(self, path: str) -> None:
        assert isinstance(path, str)
        self.__path = path

    scheme = property(fset=scheme)
    domain = property(fset=domain)
    subdomain = property(fset=subdomain)
    api_path = property(fset=api_path)
    api_version = property(fset=api_version)
    path = property(fset=path)

    def build(self):
        # Url Generation
        url: str = (
            f"{self.__scheme}://"
            f"{self.__subdomain}{'.' if self.__subdomain else ''}"
            f"{self.__domain}"
            f"/{self.__api_path}"
            f"/{self.__api_version}"
            f"/{self.__path}"
        )
        debug(f"url (unparsed): {url}")
        url = urlparse(url).geturl()
        debug(f"url   (parsed): {url}")

        return url


class API:
    """Handles the connection to the Representational State Transfer (REST)
    API of synapse and communication.
    """

    __slots__ = (
        "token",
        "domain",
        "json_format",
        "url",
        "__success_codes",
        "session",
        "__request",
    )

    def __init__(
        self, api_domain: str, api_token: str, json_format: bool = True
    ) -> None:
        """Initializes the Api class and checks, if the parameter
        are there.

        :param api_domain:  The API domain (e.g. "domain.tld")
        :param api_token:   The access token of an admin
        :return:            ``None``
        """

        assert isinstance(api_domain, str)
        assert isinstance(api_token, str)
        assert isinstance(json_format, bool)

        self.token: str = api_token
        self.domain: str = api_domain
        self.json_format: bool = json_format

        self.url: UrlBuilder = UrlBuilder(api_domain)
        self.__success_codes: Tuple[int] = (*range(200, 208), 226)

        self.session = requests.Session()

        self.__request: dict = {
            "method": "GET",
            "url": None,
            "params": None,
            "data": None,
            "headers": {
                "User-Agent": f"matrixctl{__version__}",
                "Authorization": f"Bearer {self.token}",
            },
        }

    def method(self, method):
        method = method.upper()
        assert method in {"GET", "POST", "PUT", "DELETE"}
        self.__request["method"] = method

    def params(self, params: dict):
        assert isinstance(params, dict)
        self.__request["params"] = params

    def headers(self, headers: dict):
        assert isinstance(headers, dict)

        if self.json_format:
            self.__request["headers"]["Content-Type"] = "application/json"

        self.__request["headers"].update(headers)

    def success_codes(self, codes: Iterable[int]):
        assert isinstance(codes, Iterable)
        self.__success_codes = codes

    method = property(fset=method)
    params = property(fset=params)
    headers = property(fset=headers)
    success_codes = property(fset=success_codes)

    def request(self, data: dict = None) -> requests.Response:
        """Sends a request to the synapse api with the help of the
        ``requests`` module.

        :param path:           The path of the request
        :param params:         Params of the request
        :param payload:        The payload of the request
        :param method:         The response method: ``GET``, ``POST``,
                               ``PUT``, ``DELETE`` of the request
        :param api_version:    The version of the api of the request
        :param success_codes:  A tuple with success return code of a requests
                               response
        :param json_payload:   ``True`` if the request and the response should
                               be in the json format.
        :return:               Returns the response
        """

        # Data Preparation

        if self.json_format and data is not None:
            self.__request["data"] = json.dumps(data)
        # Todo: data is not none and json_format == False
        self.__request["url"] = self.url.build()

        debug(f"Request: {self.__request}")

        response = self.session.request(**self.__request)

        debug(f"{response.json()=}")

        if response.status_code not in self.__success_codes:
            raise InternalResponseError()

        return response

    # def users(self, from_user: int = 0, show_guests: bool = False) -> JsonDict:
    #     """Gets a list of users and optional guests from the matrix instance.
    #     This method can download only 100 entries at once. To download another
    #     100 entries (99..199) you need to set the ``from_user`` argument to
    #     100.
    #
    #     **Example**
    #
    #     >>> api = Api(domain, tokenr)
    #     >>> api.users(0)
    #     # Users 0..99
    #     >>> api.users(100)
    #     # Users 100..199
    #     >>> api.users(200)
    #     # Users 200..299
    #
    #     :param from_user:    The number of the user to begin with.
    #                          (default: 0)
    #     :param show_guests:  ``True`` to show guests, ``False`` to don't
    #                          (default: ``False``)
    #     :return:             A json dict with the requestet users
    #     """
    #     path = f"/users"
    #     params = {
    #         "from": from_user,
    #         "guests": "true" if show_guests else "false",
    #     }
    #     response = self.request(path, method="GET", params=params)
    #
    #     if response.status_code not in (201, 200):
    #         error("The request was not successful.")
    #
    #     return response.json()
    #
    # def user(self, user: str) -> JsonDict:
    #     """Get detailed information about a user.
    #
    #     :param user:  The username
    #     :return:      A json dict of the requestes user
    #     """
    #     path = f"/users/{user}"
    #     response = self.request(path, method="GET")
    #
    #     if response.status_code not in (201, 200):
    #         error("The request was not successful.")
    #
    #     return response.json()

    def __enter__(self):
        """Makes it possible to be called with the ``with`` statement.
        This is currently not really needed, but unifis the way handlers are
        used.
        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Makes it possible to be called with the ``with`` statement.
        This is currently not really needed, but unifis the way handlers are
        used.
        """

        return


# vim: set ft=python :
