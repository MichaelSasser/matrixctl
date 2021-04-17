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

"""Use the functions of this module as printing helpers."""

from __future__ import annotations

from typing import Any


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


# TODO: Check if used and for what; type?; docs.
def human_readable_bool(b: Any) -> str:
    """Use this helper function to get a "yes" or "no" string from a "bool".

    Parameters
    ----------
    b : any
        The value to "convert".

    Returns
    -------
    answer : str
        ``"Yes"`` if expression is ``True``, or
        ``"False"`` if expression is ``False``.

    """
    if isinstance(b, str):
        b = int(b)

    if isinstance(b, int):
        b = bool(b)

    return "Yes" if b else "No"


# vim: set ft=python :
