# matrixctl
# Copyright (c) 2021-2023  Michael Sasser <Michael@MichaelSasser.org>
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

"""The purge-history command allows to purge historic events from the database.

Use this module to add the ``purge-histoy`` subcommand to ``matrixctl``.
"""

from __future__ import annotations

import logging

from datetime import datetime
from datetime import timezone


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def check_point_in_time(
    event_or_timestamp: str,
) -> dict[str, str | int] | None:
    """Check the the type of the point in time and set the correct body.

    Parameters
    ----------
    event_or_timestamp : str
        The event_id or timestamp (UNIX epoch, in milliseconds).

    Returns
    -------
    request_body: Dict [str, str or int]
        A dict, which can be merged with the request_body dict.

    """
    try:
        dt = datetime.fromtimestamp(
            float(event_or_timestamp) / 1000,
            tz=timezone.utc,
        )
        logger.debug("Delete until dt: %s", dt)
        return {"purge_up_to_ts": int(event_or_timestamp)}
    except (OverflowError, OSError, ValueError):
        if event_or_timestamp.startswith("$"):
            return {"purge_up_to_event_id": event_or_timestamp}
    return None


# vim: set ft=python :
