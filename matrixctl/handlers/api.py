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

import asyncio
import logging
import sys
import typing
import urllib.parse

from contextlib import suppress
from typing import Generator

import attr
import httpx

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
    data: dict[str, typing.Any] | None = None
    content: bytes | None = None
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


def _request(req: RequestBuilder) -> httpx.Response:
    """Send an  syncronus request to the synapse API and receive a response.

    Parameters
    ----------
    req : matrixctl.handlers.api.RequestBuilder
        An instance of an RequestBuilder

    Returns
    -------
    response : requests.Response
        Returns the response

    """

    logger.debug("repr: %s", repr(req))

    with httpx.Client(
        http2=True,
    ) as client:
        response: httpx.Response = client.request(
            method=req.method,
            data=req.data,
            content=req.content,
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

    logger.debug("JSON response: %s", response.json())

    logger.debug(f"Response Status Code: %d", response.status_code)
    if response.status_code not in req.success_codes:
        with suppress(Exception):
            if response.json()["errcode"] == "M_UNKNOWN_TOKEN":
                logger.critical(
                    "The server rejected your access-token. "
                    "Please make sure, your access-token is correct "
                    "and up-to-date. Your access-token will change every "
                    "time, you log out."
                )
                sys.exit(1)
        raise InternalResponseError(payload=response)

    return response


async def _async_request(req):

    logger.debug("repr: %s", repr(req))

    async with httpx.AsyncClient(http2=True) as client:
        response: httpx.Response = await client.request(
            method=req.method,
            data=req.data,
            content=req.content,
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

    logger.debug("JSON response: %s", response.json())

    logger.debug(f"Response Status Code: %d", response.status_code)
    if response.status_code not in req.success_codes:
        with suppress(Exception):
            if response.json()["errcode"] == "M_UNKNOWN_TOKEN":
                logger.critical(
                    "The server rejected your access-token. "
                    "Please make sure, your access-token is correct "
                    "and up-to-date. Your access-token will change every "
                    "time, you log out."
                )
                sys.exit(1)
        raise InternalResponseError(payload=response)
    return response


def request(
    request_config: RequestBuilder | Generator[RequestBuilder, None, None],
    concurrent_limit=4,
    raise_error=True,
) -> list[httpx.Response]:
    async def worker(
        input_queue: asyncio.Queue,
        output_queue: asyncio.Queue,
        concurrent: bool,
    ):
        while not input_queue.empty():
            idx, item = await input_queue.get()
            try:
                if concurrent:
                    output: httpx.Response = await _async_request(item)
                else:
                    output: httpx.Response = _request(item)
                await output_queue.put((idx, output))

            except Exception as err:
                await output_queue.put((idx, err))

            finally:
                input_queue.task_done()

    async def group_results(
        input_size, output_queue: asyncio.Queue, concurrent
    ):
        output = {}  # No need to sort afterwards

        for _ in range(input_size):
            idx, result = await output_queue.get()  # (idx, result)
            output[idx] = result
            output_queue.task_done()
        if concurrent:
            return [output[i] for i in range(input_size)]
        return output[0]

    async def procedure():
        nonlocal concurrent_limit
        input_queue: asyncio.Queue = asyncio.Queue()
        if isinstance(request_config, RequestBuilder):
            input_queue.put_nowait((0, request_config))
            concurrent_limit = 1
        else:
            for idx, item in enumerate(request_config):
                input_queue.put_nowait((idx, item))

        # Remember size before using Queue
        input_size = input_queue.qsize()

        # Generate task pool, and start collecting data.
        output_queue: asyncio.Queue = asyncio.Queue()
        result_task = asyncio.create_task(
            group_results(input_size, output_queue, concurrent_limit > 1)
        )
        tasks = [
            asyncio.create_task(
                worker(input_queue, output_queue, concurrent_limit > 1)
            )
            for _ in range(concurrent_limit)
        ]

        # Wait for tasks complete
        await asyncio.gather(*tasks)

        # Wait for result fetching
        results = await result_task

        # Re-raise errors
        if concurrent_limit > 1:  # if concurrent
            if raise_error and (
                errors := [
                    err for err in results if isinstance(err, Exception)
                ]
            ):
                # noinspection PyUnboundLocalVariable
                raise Exception(
                    errors
                )  # It never runs before assignment, safe to ignore.
        if raise_error and isinstance(results, Exception):
            raise Exception(results)

        return results

    return asyncio.run(procedure())


# vim: set ft=python :
