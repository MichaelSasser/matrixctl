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

"""Run "metatests" on matrixctl.

Tests:

- The version of the package should be comply with SemVer.
"""

from __future__ import annotations

import logging
import re

from packaging import version as pversion


logger = logging.getLogger(__name__)


def test_version() -> None:
    """Test, if the version matches the PyPA specification.

    Notes
    -----
    See `PyPA <https://packaging.python.org/en/latest/specifications/>`_ for
    more information.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """

    # Setup
    logger.info("Using version pattern %s", pversion.VERSION_PATTERN)

    desired = re.compile(
        r"^\s*" + pversion.VERSION_PATTERN + r"\s*$",
        re.VERBOSE | re.IGNORECASE,
    )

    # Exercise
    from matrixctl import __version__

    actual = __version__

    # Verify
    assert desired.fullmatch(actual)

    # Cleanup - None
