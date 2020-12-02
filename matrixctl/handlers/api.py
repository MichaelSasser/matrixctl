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

import json
import sys

from logging import critical
from logging import debug
from types import TracebackType
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from urllib.parse import urlparse

import requests

from matrixctl import __version__
from matrixctl.errors import InternalResponseError


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def check_type(var: Any, var_name: str, var_type: Any = str) -> None:
    if not isinstance(var, var_type):
        raise TypeError(
            f"{var_name} needs to be of type {var_type}, you have entered "
            f"{type(var)}."
        )


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

    def _scheme(self, scheme: str) -> None:
        check_type(scheme, "scheme")
        self.__scheme = scheme

    def _domain(self, domain: str) -> None:
        check_type(domain, "domain")
        self.__domain = domain

    def _subdomain(self, subdomain: str) -> None:
        check_type(subdomain, "subdomain")
        self.__subdomain = subdomain

    def _api_path(self, api_path: str) -> None:
        check_type(api_path, "api_path")
        self.__api_path = api_path

    def _api_version(self, api_version: str) -> None:
        check_type(api_version, "api_version")
        self.__api_version = api_version

    def _path(self, path: str) -> None:
        check_type(path, "path")
        self.__path = path

    scheme = property(fset=_scheme)
    domain = property(fset=_domain)
    subdomain = property(fset=_subdomain)
    api_path = property(fset=_api_path)
    api_version = property(fset=_api_version)
    path = property(fset=_path)

    def build(self) -> str:
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

    """Handle the REST API connection of synapse."""

    __slots__ = (
        "token",
        "domain",
        "json_format",
        "url",
        "__success_codes",
        "session",
        "__request",
        "__method",
        "__params",
        "__headers",
    )

    # (*range(200, 208), 226)
    RESPONSE_OK: Tuple[int, ...] = (
        200,
        201,
        202,
        203,
        204,
        205,
        206,
        207,
        226,
    )

    def __init__(
        self, domain: str, token: str, json_format: bool = True
    ) -> None:
        """Initialize the Api class and checks, if the parameter are there.

        :param api_domain:  The API domain (e.g. "domain.tld")
        :param api_token:   The access token of an admin
        :return:            ``None``
        """

        check_type(domain, "domain")
        check_type(token, "token")
        check_type(json_format, "json_format", bool)

        self.token: str = token
        self.json_format: bool = json_format

        self.url: UrlBuilder = UrlBuilder(domain)
        self.__success_codes: Tuple[int, ...] = self.__class__.RESPONSE_OK

        self.session = requests.Session()

        self.__method: str = "GET"
        self.__params: Dict[str, str] = {}
        self.__headers: Dict[str, str] = {
            "User-Agent": f"matrixctl{__version__}",
            "Authorization": f"Bearer {self.token}",
        }

    def _method(self, method: str) -> None:
        method = method.upper()
        if method not in {"GET", "POST", "PUT", "DELETE"}:
            raise ValueError(
                'method needs to be one of {"GET", "POST", "PUT", "DELETE"}, '
                f"you have entered {type(method)}."
            )
        self.__method = method

    def _params(self, params: Dict[str, str]) -> None:
        check_type(params, "params", dict)
        self.__params.update(params)

    def _headers(self, headers: Dict[str, str]) -> None:
        check_type(headers, "headers", dict)

        if self.json_format:
            self.__headers["Content-Type"] = "application/json"

        self.__headers.update(headers)

    def _success_codes(self, codes: Tuple[int]) -> None:
        check_type(codes, "codes", dict)
        self.__success_codes = codes

    method = property(fset=_method)
    params = property(fset=_params)
    headers = property(fset=_headers)
    success_codes = property(fset=_success_codes)

    def request(
        self, data: Union[str, None, Dict[str, Any]] = None
    ) -> requests.Response:
        """Send a request to the synapse API.

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
        debug("Started API request.")

        url: str = self.url.build()

        if self.json_format and data is not None:
            data = json.dumps(data)

        debug_headers = self.__headers.copy()
        # len("Bearer ") = 7
        debug_headers[
            "Authorization"
        ] = f"HIDDEN (Length={len(self.__headers['Authorization'])-7})"
        debug(f"Method: {self.__method}")
        debug(f"Headers: {debug_headers}")
        debug(f"Params: {self.__params}")
        debug(f"Data: {data}")

        response = self.session.request(
            method=self.__method,
            data=data,
            url=url,
            params=self.__params,
            headers=self.__headers,
            allow_redirects=False,
        )

        if response.status_code == 302:
            critical(
                "The api request resulted in an redirect (302). "
                "This indicates, that the API might have changed, or your "
                "playbook is misconfigured.\n"
                "Please make sure your installation of matrixctl is "
                "up-to-date and your vars.yml contains:\n\n"
                "matrix_nginx_proxy_proxy_matrix_client_redirect_root_uri_to"
                '_domain: ""'
            )
            sys.exit(1)
        if response.status_code == 404:
            critical(
                "You need to make sure, that your vars.yml contains the "
                "following excessive long line:\n\n"
                "matrix_nginx_proxy_proxy_matrix_client_api_forwarded_"
                "location_synapse_admin_api_enabled: true"
            )
            sys.exit(1)

        debug(f"{response.json()=}")

        debug(f"{response.status_code=}")
        if response.status_code not in self.__success_codes:
            try:
                if response.json()["errcode"] == "M_UNKNOWN_TOKEN":
                    critical(
                        "The server rejected your access-token. "
                        "Please make sure, your access-token is correct "
                        "and up-to-date. Your access-token will change every "
                        "time, you log out."
                    )
                    sys.exit(1)
            except Exception:  # pylint: disable=broad-except
                pass

            raise InternalResponseError(payload=response)

        return response

    def __enter__(self) -> API:
        """Use the class with the ``with`` statement`` statement.

        This is currently not really needed, but unifies the way handlers are
        used.
        """

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Use the class with the ``with`` statement`` statement.

        This is currently not really needed, but unifies the way handlers are
        used.
        """

        return


# vim: set ft=python :
