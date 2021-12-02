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

"""Create an SSH tunnel."""
from collections.abc import Iterator


from __future__ import annotations

import logging

from contextlib import contextmanager
from pathlib import Path

from sshtunnel import SSHTunnelForwarder


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


@contextmanager
def ssh_tunnel(
    host: str,
    username: str,
    remote_port: int,
    enabled: bool = True,
    port: int = 22,
    private_key: Path | str | None = None,
) -> Iterator[SSHTunnelForwarder | None]:
    """Create an SSH tunnel.

    Notes
    -----
    The tunnel will only be created, when it is enabled. If the tunnel is
    disabled (``enabled = False``), the function will yield ``None`` instead
    of the ``SSHTunnelForwarder``. The local bind port is not
    user-configurable. It can be retreaved as shown in the example.

    Examples
    --------
    >>> with ssh_tunnel(127.0.0.1, myuser, 5432) as tunnel:
    >>>     print(f"The local bind port is: {tunnel.local_bind_port}")
    The local bind port is: 8765


    Parameters
    ----------
    host : str
        The remote host e.g. ``127.0.0.1`` or ``host.domain.tld``.
    username : str
        The username of the user.
    remote_port : int
        The port of the application, which should be tunneled.
    enabled : bool, default: True
        ``True`` if the tunnel should be enabled or ``False`` if not.
    port : int, default: 22
        The ssh port
    private_key : Path or str, optioal
        The path to the private key

    Yields
    ------
    tun : sshtunnel.SSHTunnelForwarder
        The ``SSHTunnelForwarder`` object.
    None : None
        Yields none, when the tunnel is disabled (``enabled = False``).

    Returns
    -------
    None

    """
    if enabled:
        tun = SSHTunnelForwarder(
            ssh_address_or_host=(host, port),
            ssh_username=username,
            remote_bind_address=("127.0.0.1", remote_port),
            ssh_pkey=str(private_key),
        )

        try:
            tun.start()
            logger.debug(
                "SSH tunnel created using port: %s", tun.local_bind_port
            )
            yield tun
        finally:
            tun.stop()
            logger.debug("SSH tunnel closed")
        return
    yield None


# vim: set ft=python :
