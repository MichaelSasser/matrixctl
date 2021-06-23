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

"""Get access to the API of your homeserver."""

from __future__ import annotations

import json
import logging
import sys
import typing
import urllib.parse

import attr
import requests

from matrixctl import __version__
from matrixctl.errors import InternalResponseError


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


@attr.s(slots=True, auto_attribs=True, repr=False)
class RequestBuilder:

    """Build the URL for an API request."""

    token: str = attr.ib()
    domain: str = attr.ib()
    path: str = attr.ib()
    scheme: str = "https"
    subdomain: str = "matrix"
    api_path: str = "_synapse/admin"
    api_version: str = "v2"
    data: bytes | str | None | dict[str, typing.Any] = None
    method: str = "GET"
    json: bool = True
    params: dict[str, str | int] = {}
    headers: dict[str, str] = {}
    success_codes: tuple[int, ...] = (
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

    @property
    def headers_with_auth(self) -> dict[str, str]:
        """Get the headers with bearer token.

        Parameters
        ----------
        None

        Returns
        -------
        headers : dict [str, str]
            Headers with auth. token.

        """
        return self.headers | {
            "User-Agent": f"matrixctl{__version__}",
            "Authorization": f"Bearer {self.token}",
        }

    def __str__(self) -> str:
        """Build the URL.

        Parameters
        ----------
        None

        Returns
        -------
        url : str
            The URL.

        """
        url: str = (
            f"{self.scheme}://"
            f"{self.subdomain}{'.' if self.subdomain else ''}"
            f"{self.domain}"
            f"/{self.api_path}"
            f"/{self.api_version}"
            f"/{self.path}"
        )
        url = urllib.parse.urlparse(url).geturl()
        return url

    def __repr__(self) -> str:
        """Get a string representation of this class.

        Parameters
        ----------
        None

        Returns
        -------
        url : str
            Data of this class in string representation.

        """
        return (
            f"{self.__class__.__qualname__}({self.method} {self.__str__()} {{"
            f"headers={self.headers}, params={self.params}, data="
            f"{'[binary]' if isinstance(self.data, bytes) else self.data} "
            f"success_codes={self.success_codes}, json={self.json}, "
            f"token=[redacted (length={len(self.token)})])}}"
        )


def request(req: RequestBuilder) -> requests.Response:
    """Send an request to the synapse API and receive a response.

    Parameters
    ----------
    req : matrixctl.handlers.api.RequestBuilder
        An instance of an RequestBuilder

    Returns
    -------
    response : requests.Response
        Returns the response

    """
    data = req.data
    if req.json and data is not None:
        data = json.dumps(req.data)

    logger.debug(repr(req))

    response = requests.Session().request(
        method=req.method,
        data=data,
        url=str(req),
        params=req.params,
        headers=req.headers_with_auth,
        allow_redirects=False,
    )

    if response.status_code == 302:
        logger.critical(
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
        logger.critical(
            "You need to make sure, that your vars.yml contains the "
            "following excessive long line:\n\n"
            "matrix_nginx_proxy_proxy_matrix_client_api_forwarded_"
            "location_synapse_admin_api_enabled: true"
        )
        sys.exit(1)

    logger.debug(f"{response.json()=}")

    logger.debug(f"{response.status_code=}")
    if response.status_code not in req.success_codes:
        try:
            if response.json()["errcode"] == "M_UNKNOWN_TOKEN":
                logger.critical(
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


# vim: set ft=python :
