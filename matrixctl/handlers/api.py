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
import math
import typing
import urllib.parse

from collections.abc import Generator
from collections.abc import Iterable
from contextlib import suppress
from copy import deepcopy

import attr
import httpx

from matrixctl import __version__
from matrixctl.errors import ExitQWorker
from matrixctl.errors import InternalResponseError


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)

Response = httpx.Response


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
    concurrent_limit: int = 4
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
    """Send an syncronus request to the synapse API and receive a response.

    Attributes
    ----------
    req : matrixctl.handlers.api.RequestBuilder
        An instance of an RequestBuilder

    Returns
    -------
    response : httpx.Response
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
        raise ExitQWorker()  # TODO
    if response.status_code == 404:
        logger.critical(
            "You need to make sure, that your vars.yml contains the "
            "following excessive long line:\n\n"
            "matrix_nginx_proxy_proxy_matrix_client_api_forwarded_"
            "location_synapse_admin_api_enabled: true"
        )
        raise ExitQWorker()  # TODO

    logger.debug("JSON response: %s", response.json())

    logger.debug("Response Status Code: %d", response.status_code)
    if response.status_code not in req.success_codes:
        with suppress(Exception):
            if response.json()["errcode"] == "M_UNKNOWN_TOKEN":
                logger.critical(
                    "The server rejected your access-token. "
                    "Please make sure, your access-token is correct "
                    "and up-to-date. Your access-token will change every "
                    "time, you log out."
                )
                raise ExitQWorker()  # TODO
        raise InternalResponseError(payload=response)

    return response


async def _async_request(request_config: RequestBuilder) -> httpx.Response:
    """Send an asynchronous request to the synapse API and receive a response.

    Attributes
    ----------
    req : matrixctl.handlers.api.RequestBuilder
        An instance of an RequestBuilder

    Returns
    -------
    response : httpx.Response
        Returns the response

    """

    logger.debug("repr: %s", repr(request_config))

    async with httpx.AsyncClient(http2=True) as client:
        response: httpx.Response = await client.request(
            method=request_config.method,
            data=request_config.data,
            content=request_config.content,
            url=str(request_config),
            params=request_config.params,
            headers=request_config.headers_with_auth,
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
        raise ExitQWorker()  # TODO
    if response.status_code == 404:
        logger.critical(
            "You need to make sure, that your vars.yml contains the "
            "following excessive long line:\n\n"
            "matrix_nginx_proxy_proxy_matrix_client_api_forwarded_"
            "location_synapse_admin_api_enabled: true"
        )
        raise ExitQWorker()  # TODO

    logger.debug("JSON response: %s", response.json())

    logger.debug("Response Status Code: %d", response.status_code)
    if response.status_code not in request_config.success_codes:
        with suppress(Exception):
            if response.json()["errcode"] == "M_UNKNOWN_TOKEN":
                logger.critical(
                    "The server rejected your access-token. "
                    "Please make sure, your access-token is correct "
                    "and up-to-date. Your access-token will change every "
                    "time, you log out."
                )
                raise ExitQWorker()  # TODO
        raise InternalResponseError(payload=response)
    return response


class RequestStrategy(typing.NamedTuple):

    """Use this NamedTuple as request strategy data.

    This NamedTuple is only used in this module.

    """

    limit: int
    step_size: int
    concurrent_limit: int
    offset: int
    iterations: int


def preplan_request_strategy(
    limit: int, concurrent_limit: int | float, max_step_size: int = 100
) -> RequestStrategy:
    """Use this functiona as helper for optimizing asyncronous requests.

    Attributes
    ----------
    limit : int
        A user entered limit or total.
    concurrent_limit: int
        The concurrent limit from the config file.
    max_step_size : int, default=100
        The maximal step size, which is a soft limit.
        It is usualy 100, but that value might be different. Check out the API
        documentation. We usualy take the default one.

    Returns
    -------
    RequestStrategy : matrixctl.handlers.api.RequestStrategy
        A Named tuple with the RequestStrategy values.

    """
    concurrent_limit = float(concurrent_limit)

    # limit might be total.

    if limit > max_step_size:  # limit step_size
        step_size = 100
    else:
        step_size = limit

    workers: float = min(limit / step_size, concurrent_limit)

    iterations: float = limit / (workers * step_size)
    new_iterations: int = math.ceil(iterations)
    workers_temp: int = math.ceil(limit / (step_size * new_iterations))
    new_workers: int = min(workers_temp, math.ceil(concurrent_limit))
    new_step_size: int = math.ceil(limit / (new_workers * new_iterations))

    new_limit: int = new_step_size * new_workers * new_iterations  # total
    offset: int = new_limit - limit  # How many to hold back

    # Debug output
    logger.debug("concurrent_limit = %s", concurrent_limit)
    logger.debug("limit = %s", limit)
    logger.debug(
        "step_size = %s -> step_size_n = %s (soft limit = 100)",
        step_size,
        new_step_size,
    )
    logger.debug(
        "workers = %s     -> new_workers = %s (hard limit = %s)",
        workers,
        new_workers,
        concurrent_limit,
    )
    logger.debug(
        'iterations = %s -> new_iterations = %s ("unlimited")',
        iterations,
        new_iterations,
    )
    logger.debug("new_limit (true limit) = %s", new_limit)
    logger.debug("offset = %s (negative not allowed)", offset)

    if offset < 0:
        raise InternalResponseError("The offset must always be positive.")

    return RequestStrategy(
        new_limit, new_step_size, new_limit, offset, new_iterations
    )


def generate_worker_configs(
    request_config: RequestBuilder, next_token: int, limit: int
) -> Generator[RequestBuilder, None, None]:
    """Create workers for async requests (minus the already done sync reqest).

    Notes
    -----
    Warning ``Call-By-Reference`` like behavior!
    The param ``limit`` and the ``concurrent_limit`` in ``request_config``
    will get changed in this function. Make sure to only use them after using
    this function!

    Attributes
    ----------
    request_config : matrixctl.handlers.api.RequestBuilder
        An instance of an RequestBuilder from which was used for an initial
        synchronous request to get the first part of the data and the other
        two arguments from the response.
    next_token : int
        The value, which defines from where to start in the next request.
        You get this value from the response of an initial synchronous request.
    total : int
        The value which defines how many entries there are.
        You get this value from the response of an initial synchronous request.

    Yields
    ------
    request_config : matrixctl.handlers.api.RequestBuilder
        Yields a fully configured ``RequestsBuilder`` for every request that
        has to be done to get all entries.

    """
    if limit - next_token < 0:
        raise InternalResponseError(
            f"limit - next_token is negative ({limit - next_token}). "
            "Make sure that you not use generate_worker_configs() if it "
            "isn't necessary. For example with total > 100."
        )
    strategy: RequestStrategy = preplan_request_strategy(
        limit - next_token,  # minus the already queried
        concurrent_limit=request_config.concurrent_limit,
        max_step_size=limit if limit < 100 else 100,
    )
    # limit the request "globally"
    request_config.params["limit"] = strategy.step_size

    # overwrite the concurrent limit
    request_config.concurrent_limit = strategy.concurrent_limit
    # reapply next_token to get the full range back for i
    logger.debug(
        "for loop (generator):"
        f"{next_token + 1 = }, {strategy.limit + next_token + 1 = }, "
        f"{strategy.step_size = }"
    )
    for i in range(
        next_token + 1, strategy.limit + next_token + 1, strategy.step_size
    ):
        worker_config = deepcopy(request_config)  # deepcopy needed
        worker_config.params["from"] = i
        yield worker_config


@typing.overload
def request(
    request_config: Generator[RequestBuilder, None, None],
    concurrent_limit: int,
) -> list[httpx.Response]:
    """Overload for request."""


@typing.overload
def request(
    request_config: RequestBuilder, concurrent_limit: int = ...
) -> httpx.Response:
    """Overload for request."""


# flake8: noqa: C901
def request(
    request_config: RequestBuilder | Generator[RequestBuilder, None, None],
    concurrent_limit: int = 1,  # default from config is 4
) -> list[httpx.Response] | httpx.Response:
    """Make a (a)synchronous request to the synapse API and receive a response.

    Attributes
    ----------
    request_config : RequestBuilder or Generator [RequestBuilder, None, None]
        An instance of an ``RequestBuilder`` or a list of ``RequestBuilder``.
        If the function gets a ``RequestBuilder``, the request will be
        synchronous.
        If it gets a Generator, the request will be asynchronous.
    concurrent_limit : int
        The maximum of concurrent workers. (This information must be pulled
        from the config.)

    See Also
    --------
    RequestBuilder : matrixctl.handlers.api.RequestBuilder

    Returns
    -------
    response : httpx.Response
        Returns the response

    """

    async def worker(
        input_queue: asyncio.Queue[tuple[int, RequestBuilder]],
        output_queue: asyncio.Queue[
            tuple[int, httpx.Response] | tuple[int, Exception]
        ],
        concurrent: bool,
    ) -> None:
        """Use this coro as worker to make (a)synchronous request.

        Attributes
        ----------
        input_queue : asyncio.Queue
            The input queue, which provides the ``RequestBuilder``.
        output_queue : asyncio.Queue
            The output queue, which gets the responses of ther requests.
        concurrent : bool
            When ``True``, make requests concurrently.
            When ``False``, make requests synchronously.


        See Also
        --------
        RequestBuilder : matrixctl.handlers.api.RequestBuilder

        Returns
        -------
        None

        """
        output: httpx.Response
        while not input_queue.empty():
            idx, item = await input_queue.get()
            try:
                if concurrent:
                    output = await _async_request(item)
                else:
                    output = _request(item)
                await output_queue.put((idx, output))

            except Exception as err:  # skipcq: PYL-W0703
                await output_queue.put((idx, err))

            finally:
                input_queue.task_done()

    async def group_results(
        input_size: int,
        output_queue: asyncio.Queue[
            tuple[int, httpx.Response] | tuple[int, Exception]
        ],
        concurrent: bool,
    ) -> httpx.Response | list[httpx.Response]:
        """Use this coro to group the requests afterwards in a single list.

        Attributes
        ----------
        input_size : int
            The number of items in the queue.
        output_queue : asyncio.Queue
            The output queue, which holds the responses of ther requests.
        concurrent : bool
            When ``True``, make requests concurrently.
            When ``False``, make requests synchronously.

        Returns
        -------
        responses : list of httpx.Response or httpx.Response
            Depending on ``concurrent``, it is a ``httpx.Response`` if
            ``concurrent`` is true, otherwise it is a ``list`` of
            ``httpx.Response``.

        """
        output = {}  # No need to sort afterwards

        for _ in range(input_size):
            idx, result = await output_queue.get()  # (idx, result)
            output[idx] = result
            output_queue.task_done()
        if concurrent:
            return [output[i] for i in range(input_size)]
        return output[0]

    async def procedure() -> httpx.Response | list[httpx.Response]:
        """Use this coro to generate and run workers and group the responses.

        Returns
        -------
        responses : list of httpx.Response or httpx.Response
            Depending on ``concurrent_limit`` an ``request_config``.

        """

        input_queue: asyncio.Queue[tuple[int, RequestBuilder]]
        output_queue: asyncio.Queue[
            tuple[int, httpx.Response] | tuple[int, Exception]
        ]
        # output_queue: asyncio.Queue[
        #     tuple[tuple[int, httpx.Response], Exception]
        # ]
        nonlocal concurrent_limit
        input_queue = asyncio.Queue()
        if isinstance(request_config, RequestBuilder):
            input_queue.put_nowait((0, request_config))
            concurrent_limit = 1
        else:
            for idx, item in enumerate(request_config):
                input_queue.put_nowait((idx, item))

        # Remember the number of items in the queue, before using it
        input_size = input_queue.qsize()

        # Generate task pool, and start collecting data.
        output_queue = asyncio.Queue()
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
        # concurrent
        if concurrent_limit > 1 and isinstance(results, Iterable):
            if errors := [
                err for err in results if isinstance(err, Exception)
            ]:
                raise Exception(errors)
        if isinstance(results, Exception):  # Not concurrent
            raise Exception(results)

        return results

    # Use a shortpass maybe and remove everything sync above?:
    # Does not give a real benefit in time and ressources.
    if isinstance(request_config, RequestBuilder):
        return _request(request_config)
    return asyncio.run(procedure())


# vim: set ft=python :
