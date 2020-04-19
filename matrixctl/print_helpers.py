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

from typing import Any
from typing import Union


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def human_readable_bool(b: Union[Any]) -> str:
    if isinstance(b, str):
        b = int(b)

    if isinstance(b, int):
        b = bool(b)

    return "Yes" if b else "No"


# vim: set ft=python :
