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

"""Talk to the the database."""


from __future__ import annotations

import logging
import typing as t
import urllib.parse



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
            f"{self.username}:{self.password}@{self.host}:{self.port}"
            f"/{self.database}"
            f"?connect_timeout={self.timeout}"
        )
        url = urllib.parse.urlparse(url).geturl()
        return url


# vim: set ft=python :
