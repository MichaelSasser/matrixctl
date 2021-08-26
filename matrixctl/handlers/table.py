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

"""Use this handler to generate and print tables."""

from __future__ import annotations

import logging

from collections.abc import Generator
from collections.abc import Sequence


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


def get_colum_length(
    data: list[list[str]], headers: None | list[list[str]]
) -> tuple[int, ...]:
    """Transpose rows and find longest line.

    Parameters
    ----------
    data : list of list of str
        The data part of the table.
    headers : None or list of list of str
        The headers part of the table.

    Returns
    -------
    column_length_tuple : None
        A n-tuple which describes the longest srting per column. (n is the
        number of columns)

    """
    # Transpose and get max length
    column_length: Generator[int, None, None] = (
        len(max(n, key=len)) for n in zip(*data)
    )
    if headers is not None:  # Alternative path, when header is enabled
        # do the same with the header
        column_length_header: Generator[int, None, None] = (
            len(max(n, key=len)) for n in zip(*headers)
        )
        return tuple(
            max(m, n) for m, n in zip(column_length_header, column_length)
        )

    return tuple(column_length)


def transpose_newlines_to_rows(
    splitted: list[list[str]], occurences: int
) -> Generator[list[str], None, None]:
    """Transpose newlines in new rows.

    Parameters
    ----------
    splitted : list of list of str
        A list of substring-lists, splitted from one row, which contains
        newline characters. The substing-lists are containing strings,
        which have been splitted into substings.
    occurences : int
        The maximal number of newlines across the row.

    Yields
    ------
    row : list[str]
        A row for each occurence.

    """
    for i in range(occurences + 1):
        row: list[str] = []
        for column in splitted:
            try:
                row.append(column[i])
            except IndexError:
                row.append("")
        yield row


def handle_newlines(
    part: list[list[str]], newlines: dict[int, int]
) -> tuple[list[list[str]], set[int]]:
    """Update and insert new lines.

    Parameters
    ----------
    part : list of list of str
        Data or headers of the table.
    newlines : dict [int, int]
        A dictionary ``{r: n}``, where ``n`` are newlines in row ``r``.

    Returns
    -------
    part, inhibit_sep : tuple [list of list of str, set of int]
        The ``part`` contains the supplemented and updated rows.
        The ``inhibit_sep`` ``set`` contains the line numbers
        where a separator yhould be inhibited because the lines handled by
        this function are belonging together.

    """
    inhibit_sep: set[int] = set()
    offset: int = 0  # grows with every inserted line

    # occurences = the maximum number of newline chars in one row (not sum)
    for line_number, occurences in newlines.items():
        splitted = [
            column.splitlines() for column in part[line_number + offset]
        ]
        # logger.debug(f"{splitted = }")

        new_rows: Generator[
            list[str], None, None
        ] = transpose_newlines_to_rows(splitted, occurences)

        # The first new line will replace the old line
        try:
            part[line_number + offset] = next(new_rows)
            # logger.debug(f"new row = {data[line_number+offset]}")
        except StopIteration:
            logger.error("There is a bug in the table handler.")
            return part, inhibit_sep

        # The following lines will be inserted
        for additional_row in new_rows:
            # logger.debug(f"new row = {additional_row}")
            inhibit_sep.add(line_number + offset)
            offset += 1
            part.insert(line_number + offset, additional_row)

    return part, inhibit_sep


def newlines_in_row(row: list[str]) -> int:
    """Get the highest number of newlines per row.

    The highest number of newlines for a row is used to dertermine in how
    many rows the row gets expanded, to get one row per newline - 1.

    Parameters
    ----------
    row : list of str
        Data or headers of the table.

    Returns
    -------
    max_newlines : int
        The highest number of newlines ber row.

    """
    return int(max(cell.count("\n") for cell in row))  # int for mypy


def find_newlines(data: list[list[str]]) -> dict[int, int]:
    """Find newlines and return a dict with positions (key) and occurences.

    Notes
    -----
    The function only adds an entry to the dict, if there is at least one
    newline in a row.

    Parameters
    ----------
    data : list of str
        Data or headers of the table.

    Returns
    -------
    pos : dict [int, int]
        A dictionary ``{r: n}``, where ``n`` are newlines in row ``r``.

    """
    return {
        i: newlines_in_row(row)
        for i, row in enumerate(data)
        if newlines_in_row(row) > 0
    }


def format_table_row(line: list[str], max_column_len: tuple[int, ...]) -> str:
    """Format a table row into a ``str``.

    Parameters
    ----------
    line : list of str
        A data or headers row, which will be formatted to a string.
    max_column_len : tuple of int
        A n-tuple which describes the longest srting per column. (n is the
        number of columns)

    Returns
    -------
    row_string : str
        A formatted string, which represents a table row.

    """
    return (
        f"| {' | '.join(s.ljust(i) for s, i in zip(line, max_column_len))} |"
    )


def cells_to_str(part: Sequence[Sequence[str]], none: str) -> list[list[str]]:
    """Convert all cells to strings and format ``None`` values.

    Parameters
    ----------
    part : collections.abc.Sequence of collections.abc.Sequence of str
        Data or header, in which every cell will be to casted to to strings.
    none : str
        A string, which is used to replace ``None`` with the specific string.

    Returns
    -------
    part : list of list of str
    The part, where every cell is of type ``str``.

    """
    data: list[list[str]] = []
    for row in part:
        data.append([str(s if s is not None else none) for s in row])
    return data


def table(
    table_data: Sequence[Sequence[str]],
    table_headers: Sequence[str] | None = None,
    sep: bool = True,
    none: str = "-",
) -> Generator[str, None, None]:
    """Create a table from data and a optional headers.

    Parameters
    ----------
    table_data : collections.abc.Sequence of collections.abc.Sequence of str
        Data.
    table_headers : collections.abc.Sequence of str, Optional
        Headers.
    sep : bool, default = True
        ``True``, when ther should be a separator between every row of data.
    none : str, default = "-"
        A string, which is used to replace ``None`` with the specific string.

    Yields
    ------
    table : Generator [str, None, None]
    The table (row for row).

    """
    # data: list[Sequence[str]] = list(table_data)
    data: list[list[str]] = cells_to_str(table_data, none)

    headers: list[list[str]] | None = None
    if table_headers is not None:
        headers = cells_to_str([table_headers], none)

    newlines: dict[int, int] = find_newlines(data)
    if headers is not None:
        headers, _ = handle_newlines(headers, find_newlines(headers))

    data, inhibit_sep = handle_newlines(data, newlines)

    max_column_len: tuple[int, ...] = get_colum_length(data, headers)
    num_of_columns: int = len(headers) if headers is not None else len(data[0])
    num_of_rows: int = len(data)

    logger.debug(
        f"Create new Table with {num_of_columns} x {num_of_rows} Cells."
    )
    logger.debug(f"Maximal length of text per column {max_column_len}.")
    logger.debug(
        "Found newlines in data: {{r: n}}, where n are newlines in row r: "
        f"{newlines}"
    )
    logger.debug(
        f"Inhibit the creation of newlines in rows: {inhibit_sep} in data."
    )

    # The 2 in (i + 2) gives 1 extra spcae left and right of the column
    sep_line_data: str = f"|{'+'.join('-' * (i + 2) for i in max_column_len)}|"
    sep_line: str = sep_line_data.replace("|", "+")
    sep_line_header: str = sep_line.replace("-", "=")

    yield sep_line  # Top seperator (will be always printed)
    if headers is not None:
        for line in headers:
            yield format_table_row(line, max_column_len)
        yield sep_line_header

    for line_number, line in enumerate(data):
        yield format_table_row(line, max_column_len)
        if sep and line_number not in inhibit_sep:
            yield sep_line_data if line_number + 1 < num_of_rows else sep_line

    if not sep:
        yield sep_line
