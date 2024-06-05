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

"""Create handler fixtures for testing."""

from __future__ import annotations

from pathlib import Path

import pytest

from matrixctl.handlers.yaml import YAML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@pytest.fixture(scope="session", autouse=True)
def yaml() -> YAML:
    """Create a fixture for the YAML class."""
    # Setup
    yaml_: YAML = YAML({Path("tests/matrixctl/handlers/configs/config.yaml")})

    # Exercise - None

    # Verify - None

    # Cleanup -None
    return yaml_


# vim: set ft=python :
