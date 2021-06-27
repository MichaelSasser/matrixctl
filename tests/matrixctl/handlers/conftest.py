#!/usr/bin/env python
# matrixctl
# Copyright (c) 2021  Michael Sasser <Michael@MichaelSasser.org>
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

"""Create handler fixtures for testing."""

from __future__ import annotations

from pathlib import Path

import pytest

from matrixctl.handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@pytest.fixture(scope="session", autouse=True)
def toml() -> TOML:
    """Create a fixture for the TOML class."""
    # Setup
    toml_: TOML = TOML(Path("tests/matrixctl/handlers/configs/config.toml"))

    # Exercise - None

    # Verify - None

    # Cleanup -None
    return toml_


# vim: set ft=python :
