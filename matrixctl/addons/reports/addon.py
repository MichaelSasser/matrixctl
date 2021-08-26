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

"""Use this module to add the ``users`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from argparse import Namespace
from shutil import get_terminal_size
from textwrap import TextWrapper

from matrixctl.errors import InternalResponseError
from matrixctl.handlers.api import RequestBuilder
from matrixctl.handlers.api import request
from matrixctl.handlers.table import table
from matrixctl.handlers.yaml import YAML
from matrixctl.print_helpers import timestamp_to_dt
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def addon(_: Namespace, yaml: YAML) -> int:
    """Print a table of the reported events.

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
    _ : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.
    yaml : matrixctl.handlers.yaml.YAML
        The configuration file handler.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    from_event: int = 0
    events_raw: list[JsonDict] = []

    # ToDo: API bool
    req: RequestBuilder = RequestBuilder(
        token=yaml.get("api", "token"),
        domain=yaml.get("api", "domain"),
        path="event_reports",
        api_version="v1",
    )

    while True:

        req.params["from"] = from_event  # from must be in the loop
        try:
            response: JsonDict = request(req).json()
        except InternalResponseError:
            logger.critical("Could not get the event_reports table.")

            return 1

        events_raw += response["event_reports"]

        try:
            from_event = response["next_token"]
        except KeyError:
            break

    # pprint(events_raw)
    events: list[tuple[str, str]] = []

    logger.debug(f"Terminal width = {get_terminal_size().columns}")

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
                "\n".join(
                    (
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
                ),
                (
                    f"{event['id']}\n"
                    f"{dt}\n"
                    f"{event['score']}\n"
                    f"{canonical_alias}\n"
                    f"{event['name'] if event['name'] else '-'}\n"
                    f"{event['room_id']}\n"
                    f"{event['event_id']}\n"
                    f"{event['sender']}\n"
                    f"{event['user_id']}\n"
                    f"{wrapper_reason.fill(text=event['reason'])}"
                ),
            )
        )

    for line in table(events):
        print(line)

    return 0


# vim: set ft=python :
