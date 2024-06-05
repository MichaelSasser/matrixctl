#!/usr/bin/env python
# get_latest_release.py - A support script for the MatrixCtl project
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

"""Use this script in GH actions, to get the latest changelog.

The script splits the CHANGELOG.rst by the headline including
the version (example: ``0.11.2 (2021-09-26)``) and date with a
regular expression.
The first list entry at index 0 is everything before the latest entry.
The second list entry at index 1 contains the headline like in the example
above.
The third list entry contains the body of the latest entry including the
underline of the first headline.

Notes
-----
- This script is not part of the source code of MatrixCtl. It is a release
  helper script.
- After the script finished run the following command:
  ``pandoc chagelog_latest.rst --from rst --to markdown -o chagelog_latest.md``

"""

from __future__ import annotations

import logging
import re
import sys
import typing as t


from pathlib import Path


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"
__version__: str = "0.1.0"


logger = logging.getLogger(__name__)

# Modified SemVer version pattern to account for the rest of the headline
# https://regex101.com/r/pOWOBM/1  # With match groups
# https://regex101.com/r/WiHlCF/1  # without
_VERSION_PATTERN: str = (
    r"^((?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-(?:"
    r"(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?:[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
    r"\s*\((?:\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01]))\))$"
)

_HEADLINE: t.Pattern[str] = re.compile(_VERSION_PATTERN, re.MULTILINE)


def main(input_path: Path, output_path: Path) -> int:
    """Create a new file which only contains the latest changelog entry.

    Attributes
    ----------
    input_path : pathlib.Path
        The input file as ``Path()``, which is a news file created by
        towncrier.
    output_path : pathlib.Path
        The output file, which does not need to exist beforehand. The output
        will be written to this file.

    Returns
    -------
    return_code : int
        The return code of the program.
        - **0** - The program has successfully generated the outputfile.
        - **1** - An I/O error occurred.
        - **2** - The news file does not contain enough news entries.

    """
    # Read CHANGELOG.rst
    try:
        with input_path.open() as fp:
            found_headlines = _HEADLINE.split(fp.read())
    except OSError:
        logger.fatal(
            "Unable to read from the input file! input_path %s",
            input_path,
        )
        return 1

    # Check, that there are enough headlines to work with
    if len(found_headlines) < 3:  # noqa: PLR2004
        logger.fatal(
            "Unable to find enough headlines! found_headlines: %s",
            found_headlines,
        )
        return 2

    entry: str = f"{found_headlines[1]}{found_headlines[2].rstrip()}"
    logger.info("Latest entry:\n%s", entry)

    # Write changelog_latest.rst
    try:
        with output_path.open("w") as fp:
            fp.write(entry)
    except OSError:
        logger.fatal(
            "Unable to write to the output file! output_path: %s",
            output_path,
        )
        return 1

    return 0


if __name__ == "__main__":
    # setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s:%(lineno)d %(levelname)s - %(message)s",
    )

    # The path to the project root
    project_root_path: Path = Path(__file__).resolve().parent.parent

    input_: Path = project_root_path / "CHANGELOG.rst"
    output: Path = project_root_path / "chagelog_latest.rst"

    sys.exit(main(input_, output))

# vim: set ft=python :
