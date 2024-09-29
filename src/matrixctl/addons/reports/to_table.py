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

"""Use this module to add the ``rooms`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from collections.abc import Generator
from shutil import get_terminal_size
from textwrap import TextWrapper

from matrixctl.handlers.table import table
from matrixctl.print_helpers import timestamp_to_dt
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

TABLE_HEADERS: tuple[str, ...] = (
    "ID",
    "Date",
    "Time",
    "Score",
    "Canonical Alias",
    "Room Name",
    "Room ID",
    "Event ID",
    "Defendant",
    "Plaintiff",
    "Reason",
)

logger = logging.getLogger(__name__)


def to_table(events_raw: list[JsonDict]) -> Generator[str, None, None]:
    """Use this function as helper to pint the events as table.

    Examples
    --------
    .. code-block:: console

       $ matrixctl reports
       +-----------------+----------------------------------------------+
       | ID              | 2                                            |
       | Date            | 2021-05-08                                   |
       | Time            | 21:04:55                                     |
       | Score           | -100                                         |
       | Canonical Alias | -                                            |
       | Room Name       | SomeRoom                                     |
       | Room ID         | !AbCdEfGhIjKlMnOpQr:domain.tld               |
       | Event ID        | $Q_sksd348jaidj93jf9ojwef9h329ofijewhf932h9f |
       | Defendant       | @mallory:matrix.org                          |
       | Plaintiff       | @alice:myhomeverver.tld                      |
       | Reason          | Likes JavaScript                             |
       |-----------------+----------------------------------------------|
       | ID              | 1                                            |
       | Date            | 2020-08-15                                   |
       | Time            | 09:09:57                                     |
       | Score           | -100                                         |
       | Canonical Alias | -                                            |
       | Room Name       | -                                            |
       | Room ID         | !AbCdEfGhIjKlMnOpQr:matrix.org               |
       | Event ID        | $123456789012345678901:matrix.org            |
       | Defendant       | @eve:matrix.org                              |
       | Plaintiff       | @bob:myhomeserver.tld                        |
       | Reason          | Hates The Office (US)                        |
       +-----------------+----------------------------------------------+

    Parameters
    ----------
    events_raw : list of matrixctl.typehints.JsonDict
        A list of events from the API.

    Yields
    ------
    table_lines : str
        The table lines.

    """
    events: list[tuple[str, str]] = []

    logger.debug("Terminal width: %s", get_terminal_size().columns)

    wrapper_reason = TextWrapper(
        width=get_terminal_size().columns - 20,  # is const.
        drop_whitespace=True,
        break_long_words=True,
    )

    for event in events_raw:
        dt: str = timestamp_to_dt(event["received_ts"], "\n")
        canonical_alias: str = (
            event["canonical_alias"]
            if event["canonical_alias"] is not None
            else "-"
        )

        events.append(
            (
                "\n".join(TABLE_HEADERS),
                (
                    f"{event['id']}\n"
                    f"{dt}\n"
                    f"{event['score']}\n"
                    f"{canonical_alias}\n"
                    f"{event['name'] or '-'}\n"
                    f"{event['room_id']}\n"
                    f"{event['event_id']}\n"
                    f"{event['sender']}\n"
                    f"{event['user_id']}\n"
                    f"{wrapper_reason.fill(text=event['reason'])}"
                ),
            ),
        )
    return table(events)


# vim: set ft=python :
