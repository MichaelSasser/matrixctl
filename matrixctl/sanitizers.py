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

import logging
import re
import typing as t


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


EVENT_PATTERN: t.Pattern[str] = re.compile(r"^\$[0-9a-zA-Z.=_-]{1,255}$")


def sanitize_event_identifier(event_identifier: str) -> bool:
    """Sanitize an event identifier.

    Parameters
    ----------
    event_identifier : str
        The event identifier to sanitize

    Returns
    -------
    result : bool
        ``True`` if the event identifier has a valid format, ``False``, if not.

    """
    if EVENT_PATTERN.match(event_identifier):
        return True
    logger.error(
        "The given event_identifier has an invalid format. Please make sure"
        " you use one with the correct format. For example:"
        " $tjeDdqYAk9BDLAUcniGUy640e_D9TrWU2RmCksJQQEQ"
    )
    return False


# vim: set ft=python :
