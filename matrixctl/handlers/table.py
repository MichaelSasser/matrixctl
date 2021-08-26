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
    data: list[list[str]], header: list[list[str]] | None
) -> tuple[int, ...]:
    """Transpose rows and find longest line."""
    # Transpose and get max length
    column_length: Generator[int, None, None] = (
        len(max(n, key=len)) for n in zip(*data)
    )
    if header is not None:  # Alternative path, when header is enabled
        # do the same with the header
        column_length_header: Generator[int, None, None] = (
            len(max(n, key=len)) for n in zip(*header)
        )
        return tuple(
            max(m, n) for m, n in zip(column_length_header, column_length)
        )

    return tuple(column_length)


def transpose_newlines_to_rows(
    splitted: list[list[str]], occurences: int
) -> Generator[list[str], None, None]:
    """Transpose newlines in new rows."""
    for i in range(occurences + 1):
        row: list[str] = []
        for column in splitted:
            try:
                row.append(column[i])
            except IndexError:
                row.append("")
        yield row


def handle_newlines(
    data: list[list[str]], newlines: dict[int, int]
) -> tuple[list[list[str]], set[int]]:
    """Update and insert new lines."""
    inhibit_sep: set[int] = set()
    offset: int = 0  # grows with every inserted line

    # occurences = the maximum number of newline chars in one row (not sum)
    for line_number, occurences in newlines.items():
        splitted = [
            column.splitlines() for column in data[line_number + offset]
        ]
        # logger.debug(f"{splitted = }")

        new_rows: Generator[
            list[str], None, None
        ] = transpose_newlines_to_rows(splitted, occurences)

        # The first new line will replace the old line
        try:
            data[line_number + offset] = next(new_rows)
            # logger.debug(f"new row = {data[line_number+offset]}")
        except StopIteration:
            logger.error("There is a bug in the table handler.")
            return data, inhibit_sep

        # The following lines will be inserted
        for additional_row in new_rows:
            # logger.debug(f"new row = {additional_row}")
            inhibit_sep.add(line_number + offset)
            offset += 1
            data.insert(line_number + offset, additional_row)

    return data, inhibit_sep


def newlines_in_row(row: list[str]) -> int:
    """Get the highest number of newlines per row."""
    return int(max(cell.count("\n") for cell in row))  # int for mypy


def find_newlines(data: list[list[str]]) -> dict[int, int]:
    """Find newlines and return a dict with positions (key) and occurences."""
    return {
        i: newlines_in_row(row)
        for i, row in enumerate(data)
        if newlines_in_row(row) > 0
    }


def create_table_row(line: list[str], max_column_len: tuple[int, ...]) -> str:
    """Create a table row."""
    return (
        f"| {' | '.join(s.ljust(i) for s, i in zip(line, max_column_len))} |"
    )


def cells_to_str(rows: Sequence[Sequence[str]], none: str) -> list[list[str]]:
    """Convert all cells to strings."""
    data: list[list[str]] = []
    for row in rows:
        data.append([str(s if s is not None else none) for s in row])
    return data


def table(
    table_data: Sequence[Sequence[str]],
    table_headers: Sequence[str] | None = None,
    sep: bool = True,
    none: str = "-",
) -> Generator[str, None, None]:
    """Create a table from data and a optional headers."""
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
            yield create_table_row(line, max_column_len)
        yield sep_line_header

    for line_number, line in enumerate(data):
        yield create_table_row(line, max_column_len)
        if sep and line_number not in inhibit_sep:
            yield sep_line_data if line_number + 1 < num_of_rows else sep_line

    if not sep:
        yield sep_line
