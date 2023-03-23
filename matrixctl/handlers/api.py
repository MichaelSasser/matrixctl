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
import sys
import typing as t
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

InputQueueType = asyncio.Queue[tuple[int, "RequestBuilder", httpx.AsyncClient]]
OutputQueueType = asyncio.Queue[
    t.Union[tuple[int, httpx.Response], tuple[int, Exception]]
]


class RequestStrategy(t.NamedTuple):

    """Use this NamedTuple as request strategy data.

    This NamedTuple is only used in this module.

    """

    limit: int
    step_size: int
    concurrent_limit: int
    offset: int
    iterations: int


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
    data: t.Optional[dict[str, t.Any]] = None  # just key/value store
    json: t.Optional[dict[str, t.Any]] = None  # json
    content: t.Optional[t.Union[str, bytes, Iterable[bytes]]] = None  # bytes
    method: str = "GET"
    params: dict[str, t.Union[str, int]] = {}
    headers: dict[str, str] = {}  # Cannot be none with MatrixCtl
    concurrent_limit: int = 4
    timeout: float = 5.0  # seconds
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
        return urllib.parse.urlparse(url).geturl()

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
        headers = self.headers | {
            "User-Agent": f"matrixctl{__version__}",
            "Authorization": "Bearer [redacted]",
        }

        return (
            f"{self.__class__.__qualname__}({self.method} {self.__str__()} {{"
            f"headers={headers}, params={self.params}, data="
            f"{'[binary]' if isinstance(self.data, bytes) else self.data} "
            f"success_codes={self.success_codes}, json={self.json}, "
            f"token=[redacted (length={len(self.token)})], "
            f"timeout={self.timeout}, "
            f"concurrent_limit={self.concurrent_limit})}}"
        )


def preplan_request_strategy(
    limit: int, concurrent_limit: int | float, max_step_size: int = 100
) -> RequestStrategy:
    """Use this functiona as helper for optimizing asynchronous requests.

    Attributes
    ----------
    limit : int
        A user entered limit or total.
    concurrent_limit: int
        The concurrent limit from the config file.
    max_step_size : int, default=100
        The maximal step size, which is a soft limit.
        It is usually 100, but that value might be different. Check out the API
        documentation. We usually take the default one.

    Returns
    -------
    RequestStrategy : matrixctl.handlers.api.RequestStrategy
        A Named tuple with the RequestStrategy values.

    """
    concurrent_limit = float(concurrent_limit)

    # limit might be total.

    step_size: int = 100 if limit > max_step_size else limit
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
    """Create workers for async requests (minus the already done sync request).

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
        max_step_size=min(limit, 100),
    )
    # limit the request "globally"
    request_config.params["limit"] = strategy.step_size

    # overwrite the concurrent limit
    request_config.concurrent_limit = strategy.concurrent_limit
    # reapply next_token to get the full range back for i
    logger.debug(
        "for loop (generator):"
        "next_token + 1 = %s , strategy.limit + next_token + 1 = %s, "
        "strategy.step_size = %s",
        next_token + 1,
        strategy.limit + next_token + 1,
        strategy.step_size,
    )
    for i in range(
        next_token + 1, strategy.limit + next_token + 1, strategy.step_size
    ):
        worker_config = deepcopy(request_config)  # deepcopy needed
        worker_config.params["from"] = i
        yield worker_config


async def async_worker(
    input_queue: InputQueueType, output_queue: OutputQueueType
) -> None:
    """Use this coro as worker to make (a)synchronous request.

    Attributes
    ----------
    input_queue : asyncio.Queue
        The input queue, which provides the ``RequestBuilder``.
    output_queue : asyncio.Queue
        The output queue, which gets the responses of there requests.


    See Also
    --------
    RequestBuilder : matrixctl.handlers.api.RequestBuilder

    Returns
    -------
    None

    """
    output: httpx.Response
    while not input_queue.empty():
        idx, item, client = await input_queue.get()
        try:
            output = await _arequest(item, client)
            await output_queue.put((idx, output))

        # Capture all exceptions and put them into the output queue
        except Exception as err:  # skipcq: PYL-W0703
            await output_queue.put((idx, err))

        finally:
            input_queue.task_done()


async def group_async_results(
    input_size: int, output_queue: OutputQueueType
) -> list[Exception | httpx.Response]:
    """Use this coro to group the requests afterwards in a single list.

    Attributes
    ----------
    input_size : int
        The number of items in the queue.
    output_queue : asyncio.Queue
        The output queue, which holds the responses of there requests.
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
    return [output[i] for i in range(input_size)]


@t.overload
async def exec_async_request(
    request_config: Generator[RequestBuilder, None, None],
) -> list[httpx.Response]:
    """Overload for request."""


@t.overload
async def exec_async_request(request_config: RequestBuilder) -> httpx.Response:
    """Overload for request."""


async def exec_async_request(
    request_config: RequestBuilder | Generator[RequestBuilder, None, None]
) -> httpx.Response | list[httpx.Response]:
    """Use this coro to generate and run workers and group the responses.

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
    responses : list of httpx.Response or httpx.Response
        Depending on ``concurrent_limit`` an ``request_config``.

    """
    concurrent_limit: int = 1
    client: httpx.AsyncClient = httpx.AsyncClient(http2=True)

    input_queue: InputQueueType = asyncio.Queue()

    if isinstance(request_config, RequestBuilder):
        input_queue.put_nowait((0, request_config, client))
    else:
        # get the concurrent_limit from the first request_config
        try:
            first_request_config = next(request_config)
        except StopIteration:
            return []
        concurrent_limit = first_request_config.concurrent_limit
        input_queue.put_nowait((0, first_request_config, client))

        for idx, item in enumerate(request_config, 1):
            input_queue.put_nowait((idx, item, client))

    # Remember the number of items in the queue, before using it
    input_size = input_queue.qsize()

    # Generate task pool, and start collecting data.
    output_queue: OutputQueueType = asyncio.Queue()
    result_task = asyncio.create_task(
        group_async_results(input_size, output_queue)
    )
    tasks = [
        asyncio.create_task(async_worker(input_queue, output_queue))
        for _ in range(concurrent_limit)
    ]

    # Wait for tasks complete
    await asyncio.gather(*tasks)
    await client.aclose()  # close the client

    # Wait for result fetching
    results = await result_task

    # A handled result is one without exceptions
    # Re-raise errors
    # concurrent
    errors: list[Exception]
    if isinstance(results, Iterable):
        if errors := [err for err in results if isinstance(err, Exception)]:
            raise Exception(errors)
        return t.cast(list[httpx.Response], results)
    if isinstance(results, Exception):  # Not concurrent
        raise Exception(results)
    return t.cast(httpx.Response, results)


@t.overload
def request(
    request_config: Generator[RequestBuilder, None, None],
) -> list[httpx.Response]:
    """Overload for request."""


@t.overload
def request(request_config: RequestBuilder) -> httpx.Response:
    """Overload for request."""


# flake8: noqa: C901
def request(
    request_config: RequestBuilder | Generator[RequestBuilder, None, None],
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

    async def gen_async_request() -> list[httpx.Response] | httpx.Response:
        """Use as helper for executing an async request."""
        nonlocal request_config
        # cast because mypy doesn't recognize the return type of
        # exec_async_request
        return t.cast(
            t.Union[list[httpx.Response], httpx.Response],
            await exec_async_request(request_config),
        )

    # This is needed because here is decided, if the request was meant to be
    # async or sync. Even though a request was meant to be async, it may
    # be still sync (which is determined during preplanning. In case it is
    # meant to be async, but is still sync, the output will be a list so the
    # addon doesn't need to check that again.
    if isinstance(request_config, RequestBuilder):
        return _request(request_config)
    return asyncio.run(gen_async_request())


def _request(request_config: RequestBuilder) -> httpx.Response | t.NoReturn:
    """Send an synchronous request to the synapse API and receive a response.

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

    # There is some weird stuff going on in httpx. It is set to None by default
    with httpx.Client(http2=True, timeout=request_config.timeout) as client:
        response: httpx.Response = client.request(
            method=request_config.method,
            data=request_config.data,  # type: ignore
            json=request_config.json,
            content=request_config.content,  # type: ignore
            url=str(request_config),
            params=request_config.params,
            headers=request_config.headers_with_auth,
            follow_redirects=False,
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
            "The server returned an 404 error. This can have multiple causes."
            " One of them is, you try to request a resource, which does not or"
            " no longer exist. Another one is, your API endpoint is disabled."
            " Make sure, that your vars.yml contains the following excessive"
            " long"
            " line:\n\nmatrix_nginx_proxy_proxy_matrix_client_api_forwarded_location_synapse_admin_api_enabled:"
            " true"
        )
        sys.exit(1)

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
                sys.exit(1)
        raise InternalResponseError(payload=response)

    return response


async def _arequest(
    request_config: RequestBuilder, client: httpx.AsyncClient
) -> httpx.Response:
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

    # There is some weird stuff going on in httpx. It is set to None by default
    response: httpx.Response = await client.request(
        method=request_config.method,
        data=request_config.data,  # type: ignore
        json=request_config.json,
        content=request_config.content,  # type: ignore
        url=str(request_config),
        params=request_config.params,
        headers=request_config.headers_with_auth,
        timeout=request_config.timeout,
        follow_redirects=False,
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
            "The server returned an 404 error. This can have multiple causes."
            " One of them is, you try to request a resource, which does not or"
            " no longer exist. Another one is, your API endpoint is disabled."
            " Make sure, that your vars.yml contains the following excessive"
            " long"
            " line:\n\nmatrix_nginx_proxy_proxy_matrix_client_api_forwarded_location_synapse_admin_api_enabled:"
            " true"
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


# vim: set ft=python :
