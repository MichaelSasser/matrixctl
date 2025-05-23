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

"""Test the yaml handler."""

from __future__ import annotations

import pytest

from matrixctl.handlers.yaml import YAML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


# TODO: Test debug output


def test_get_ansible_playbook(yaml: YAML) -> None:
    """Test ansible -> playbook."""

    # Setup
    desired: str = "/path/to/ansible/playbook"

    # Exercise
    actual: str = yaml.get("server", "ansible", "playbook")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_synapse_playbook(yaml: YAML) -> None:
    """Test synapse -> playbook."""

    # Setup
    desired: str = "/path/to/synapse/playbook"

    # Exercise
    actual: str = yaml.get("server", "synapse", "playbook")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_api_domain(yaml: YAML) -> None:
    """Test api -> domain."""

    # Setup
    desired: str = "example.com"

    # Exercise
    actual: str = yaml.get("server", "api", "domain")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_api_username(yaml: YAML) -> None:
    """Test api -> username."""

    # Setup
    desired: str = "johndoe"

    # Exercise
    actual: str = yaml.get("server", "api", "username")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_api_token(yaml: YAML) -> None:
    """Test api -> token."""

    # Setup
    desired: str = (
        "MDAxasdfY2F0aW9uIG1pY2hhZWxzYXNzZXIub3JnCjAwMTNpZGVudGlmaWVyIGtleQowM"
        "DEwY2lkIGdlbiA9IDEKMDAyZGNpZCB1c2VyX2lkID0gQG1pY2hhZWw6bWljaGFlbHNhc3"
        "Nlci5vcmcKMDAxNmNpZCB0eXBlID0gYWNjZXNzCjAwMjFjaWQgbm9uY2UgPSB1cWJ2Tys"
        "1VlFyMUl3N0J1CjAwMmZzaWduYXR1cmUgeTBHhFmQrXiWjop8gQvg8I8ZuSHbEuII8wp3"
        "YrAKEa4K"
    )

    # Exercise
    actual: str = yaml.get("server", "api", "token")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_ssh_address(yaml: YAML) -> None:
    """Test ssh -> address."""

    # Setup
    desired: str = "matrix.example.com"

    # Exercise
    actual: str = yaml.get("server", "ssh", "address")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_ssh_port(yaml: YAML) -> None:
    """Test ssh -> port."""

    # Setup
    desired: int = 22
    desired_type: type = int

    # Exercise
    actual: int = yaml.get("server", "ssh", "port")

    # Verify
    assert actual == desired
    assert isinstance(actual, desired_type)

    # Cleanup - None


def test_get_ssh_user(yaml: YAML) -> None:
    """Test ssh -> user."""

    # Setup
    desired: str = "john"

    # Exercise
    actual: str = yaml.get("server", "ssh", "user")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_ui_image_enabled(yaml: YAML) -> None:
    """Test ui -> image -> enabled."""

    # Setup
    desired: bool = True

    # Exercise
    actual: bool = yaml.get("ui", "image", "enabled")

    # Verify
    assert actual == desired

    # Cleanup - None
    #


def test_get_ui_image_scale_factor(yaml: YAML) -> None:
    """Test ui -> image -> scale_factor."""

    # Setup
    desired: float = 2.0

    # Exercise
    actual: float = yaml.get("ui", "image", "scale_factor")

    # Verify
    assert pytest.approx(actual, 0.1) == desired

    # Cleanup - None


def test_get_ui_image_max_height_of_terminal(yaml: YAML) -> None:
    """Test ui -> image -> max_height_of_terminal."""

    # Setup
    desired: float = 0.33

    # Exercise
    actual: float = yaml.get("ui", "image", "max_height_of_terminal")

    # Verify
    assert pytest.approx(actual, 0.1) == desired

    # Cleanup - None


# vim: set ft=python :
