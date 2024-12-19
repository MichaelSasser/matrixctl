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
import sys
import typing as t

from collections.abc import Generator
from datetime import datetime
from datetime import timezone

from matrixctl.handlers.table import table
from matrixctl.print_helpers import human_readable_bool
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def make_human_readable(
    k: str,
    user_dict: dict[str, str],
    len_domain: int,
) -> tuple[str, str]:
    """Make a key/value pair of a ``user`` (line) human readable, by modifying.

    Notes
    -----
    This function is used as helper by ``matrixctl.user.generate_user_tables``.

    Parameters
    ----------
    k : str
        The key
    user_dict : `dict` [`str`, `typing.Any`]
        The line as dict, a JSON string which was converted to a Python
        dictionary. (This is not a ``Collections.UserDict``)
    len_domain : int
        The length in characters of the domain.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """

    key: str | None = None
    value: str

    if k == "name":
        value = str(user_dict[k][1:-len_domain])
    elif k == "is_guest":
        value = human_readable_bool(user_dict[k])
        key = "Guest"
    elif k in {"admin", "deactivated"}:
        value = human_readable_bool(user_dict[k])
    elif k.endswith("_ts"):
        try:
            value = str(
                datetime.fromtimestamp(float(user_dict[k]), tz=timezone.utc),
            )
        except ValueError:  # Some of them are in ms now
            value = str(
                datetime.fromtimestamp(
                    float(user_dict[k]) / 1000.0,
                    tz=timezone.utc,
                ),
            )
        except TypeError:
            value = "-"
    elif k.endswith("_at"):
        value = str(
            datetime.fromtimestamp(
                float(user_dict[k]) / 1000.0,
                tz=timezone.utc,
            ),
        )

    else:
        value = user_dict[k]

    if key is None:
        key = k.replace("_", " ").title()

    return key, value


def generate_user_tables(
    user_dict: dict[str, t.Any],
    len_domain: int,
) -> list[list[tuple[str, str]]]:
    """Generate a main user table and threepid user tables.

    The function gnerates first a main user table and then for every threepid
    a additional table from a ``user_dict``.
    It renames and makes the output human readable.

    Notes
    -----
    This function is a recursive function.

    Parameters
    ----------
    user_dict : `dict` [`str`, `typing.Any`]
        The line as dict, a JSON string which was converted to a Python
        dictionary. (This is not a ``Collections.UserDict``)
    len_domain : int
        The length in characters of the domain.

    Returns
    -------
    err_code : int
        A list in the format: ``[[main], threepids_0, ... ,threepids_n]``

    """

    table_: list[list[tuple[str, str]]] = [[]]

    for k, v in user_dict.items():
        if k == "errcode":
            logger.error("There is no user with that username.")
            sys.exit(1)

        if k == "threepids":
            for tk in v:
                ret: list[list[tuple[str, str]]] = generate_user_tables(
                    tk,
                    len_domain,
                )
                table_.append(ret[0])

            continue  # Don't add threepids to "table"

        table_[0].append(make_human_readable(k, user_dict, len_domain))

    return table_


def to_table(
    user_dict: JsonDict,
    len_domain: int,
) -> Generator[str, None, None]:
    """Use this function as helper to pint the room table.

    Parameters
    ----------
    user_dict : matrixctl.typehints.JsonDict
        The user data from the API
    len_domain : int
        The length of the homeservers domain.

    Yields
    ------
    table_lines : str
        The table lines.

    """
    user_tables = generate_user_tables(user_dict, len_domain)

    logger.debug("User: users_table = %s", user_tables)

    for num, table_ in enumerate(user_tables):
        if num < 1:
            yield "User:"
        else:
            yield "\nThreepid:"
        yield from table(table_, sep=False)


# vim: set ft=python :
