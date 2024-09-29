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

"""Talk to the the database."""

from __future__ import annotations

import logging
import sys
import typing as t
import urllib.parse

from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
import sshtunnel

from .yaml import YAML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


class DBConnectionBuilder(t.NamedTuple):
    """Build the URL for an API request."""

    host: str
    database: str
    username: str
    password: str
    port: int = 5432
    timeout: int = 10
    scheme: str = "postgresql"

    def __str__(self: DBConnectionBuilder) -> str:
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
            f"{self.username}:{self.password}@{self.host}:{self.port}"
            f"/{self.database}"
            f"?connect_timeout={self.timeout}"
        )
        return urllib.parse.urlparse(url).geturl()


@contextmanager
def ssh_tunnel(
    host: str,
    username: str,
    remote_port: int,
    port: int = 22,
    *,
    enabled: bool = True,
) -> Iterator[int | None]:
    """Create an SSH tunnel.

    Notes
    -----
    The tunnel will only be created, when it is enabled. If the tunnel is
    disabled (``enabled = False``), the function will yield ``None`` instead
    of the local bind port.

    Examples
    --------
    .. code-block:: python

       with ssh_tunnel("127.0.0.1", myuser, 5432) as remote_port:
           print(f"The local bind port is: {local_bind_port}")
       # The local bind port is: 8765

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
        The path to the private key (Currently Disabled)

    Yields
    ------
    tun : int
        The remote port
    None : None
        Yields none, when the tunnel is disabled (``enabled = False``).

    """
    if enabled:
        tun = sshtunnel.SSHTunnelForwarder(
            ssh_address_or_host=(host, port),
            ssh_username=username,
            remote_bind_address=("127.0.0.1", remote_port),
            ssh_pkey=None,
            logger=logging.getLogger(sshtunnel.__name__),
        )

        try:
            tun.start()
            logger.debug(
                "SSH tunnel created using port: %s",
                tun.local_bind_port,
            )
            yield tun.local_bind_port
        finally:
            tun.stop()
            logger.debug("SSH tunnel closed")
        return
    yield None


@contextmanager
def db_connect(yaml: YAML) -> Iterator[psycopg.Connection]:
    """Connect to a PostgreSQL database.

    Parameters
    ----------
    yaml : matrixctl.handlers.yaml.YAML
        The configuration file handler.

    Yields
    ------
    conn : psycopg.Connection
        A new ``Connection`` instance.

    """
    with ssh_tunnel(
        host=yaml.get("server", "ssh", "address"),
        port=int(yaml.get("server", "ssh", "port")),
        username=yaml.get("server", "ssh", "user"),
        remote_port=yaml.get("server", "database", "port"),
        enabled=yaml.get("server", "database", "tunnel"),
        # skipcq PY-W0069
    ) as local_bind_port:
        connection_uri = DBConnectionBuilder(
            host=(
                "127.0.0.1"
                if yaml.get("server", "database", "tunnel")
                else yaml.get("server", "ssh", "address")
            ),
            port=int(
                local_bind_port or yaml.get("server", "database", "port"),
            ),
            username=yaml.get("server", "database", "synapse_user"),
            password=yaml.get("server", "database", "synapse_password"),
            database=yaml.get("server", "database", "synapse_database"),
        )
        conn = psycopg.connect(str(connection_uri))
        try:
            yield conn
        except BaseException:  # skipcq: PYL-W0703
            logger.exception("Rollback initiated.")
            conn.rollback()
            sys.exit(1)
        else:
            conn.commit()
            logger.debug("successful -> commit")
        finally:
            conn.close()
            logger.debug("Connection to the Database has been closed.")


# vim: set ft=python :
