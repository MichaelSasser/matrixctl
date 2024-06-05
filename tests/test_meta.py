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

import re

from matrixctl import __version__


def test_version() -> None:
    """Test, if the version matches SemVer.

    Notes
    -----
    The regular expression is from `SemVer.org
    <https://semver.org/spec/v2.0.0.html#is-there-a-suggested-regular-
    expression-regex-to-check-a-semver-string>`_.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    # Setup
    desired = re.compile(
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\."
        r"(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-]"
        r"[0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
        r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
    )

    # Exercise
    actual = __version__

    # Verify
    assert desired.fullmatch(actual)

    # Cleanup - None
