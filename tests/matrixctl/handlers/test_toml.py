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

"""Test the toml handler."""

from __future__ import annotations

from matrixctl.handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


# TODO: Test debug output


def test_get_ansible_playbook(toml: TOML) -> None:
    """Test [ANSIBLE] -> Playbook."""

    # Setup
    desired: str = "/path/to/ansible/playbook"

    # Exercise
    actual: str = toml.get("ANSIBLE", "Playbook")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_synapse_playbook(toml: TOML) -> None:
    """Test [SYNAPSE] -> Playbook."""

    # Setup
    desired: str = "/path/to/synapse/playbook"

    # Exercise
    actual: str = toml.get("SYNAPSE", "Playbook")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_api_domain(toml: TOML) -> None:
    """Test [API] -> Domain."""

    # Setup
    desired: str = "example.com"

    # Exercise
    actual: str = toml.get("API", "Domain")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_api_username(toml: TOML) -> None:
    """Test [API] -> Username."""

    # Setup
    desired: str = "johndoe"

    # Exercise
    actual: str = toml.get("API", "Username")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_api_token(toml: TOML) -> None:
    """Test [API] -> Token."""

    # Setup
    desired: str = (
        "MDAxasdfY2F0aW9uIG1pY2hhZWxzYXNzZXIub3JnCjAwMTNpZGVudGlmaWVyIGtleQowM"
        "DEwY2lkIGdlbiA9IDEKMDAyZGNpZCB1c2VyX2lkID0gQG1pY2hhZWw6bWljaGFlbHNhc3"
        "Nlci5vcmcKMDAxNmNpZCB0eXBlID0gYWNjZXNzCjAwMjFjaWQgbm9uY2UgPSB1cWJ2Tys"
        "1VlFyMUl3N0J1CjAwMmZzaWduYXR1cmUgeTBHhFmQrXiWjop8gQvg8I8ZuSHbEuII8wp3"
        "YrAKEa4K"
    )

    # Exercise
    actual: str = toml.get("API", "Token")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_ssh_address(toml: TOML) -> None:
    """Test [SSH] -> Address."""

    # Setup
    desired: str = "matrix.example.com"

    # Exercise
    actual: str = toml.get("SSH", "Address")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_get_ssh_port(toml: TOML) -> None:
    """Test [SSH] -> Port."""

    # Setup
    desired: int = 22
    desired_type: type = int

    # Exercise
    actual: int = toml.get("SSH", "Port")

    # Verify
    assert actual == desired
    assert isinstance(actual, desired_type)

    # Cleanup - None


def test_get_ssh_user(toml: TOML) -> None:
    """Test [SSH] -> User."""

    # Setup
    desired: str = "john"

    # Exercise
    actual: str = toml.get("SSH", "User")

    # Verify
    assert actual == desired

    # Cleanup - None


def test_str(toml: TOML) -> None:
    """Test __str__()."""

    # Setup
    desired: str = (
        "{'ANSIBLE': {'Playbook': '/path/to/ansible/playbook'}, 'SYNAPSE':"
        " {'Playbook': '/path/to/synapse/playbook'}, 'API': {'Domain': "
        "'example.com', 'Username': 'johndoe', 'Token': "
        "'MDAxasdfY2F0aW9uIG1pY2hhZWxzYXNzZXIub3JnCjAwMTNpZGVudGlmaWVyIGtleQo"
        "wMDEwY2lkIGdlbiA9IDEKMDAyZGNpZCB1c2VyX2lkID0gQG1pY2hhZWw6bWljaGFlbHN"
        "hc3Nlci5vcmcKMDAxNmNpZCB0eXBlID0gYWNjZXNzCjAwMjFjaWQgbm9uY2UgPSB1cWJ"
        "2Tys1VlFyMUl3N0J1CjAwMmZzaWduYXR1cmUgeTBHhFmQrXiWjop8gQvg8I8ZuSHbEuI"
        "I8wp3YrAKEa4K'}, 'SSH': {'Address': 'matrix.example.com', 'Port': "
        "22, 'User': 'john'}}"
    )

    # Exercise
    actual: str = str(toml)

    # Verify
    assert actual == desired

    # Cleanup - None


def test_repr(toml: TOML) -> None:
    """Test __repr__()."""

    # Setup
    desired: str = (
        "{'ANSIBLE': {'Playbook': '/path/to/ansible/playbook'}, 'SYNAPSE':"
        " {'Playbook': '/path/to/synapse/playbook'}, 'API': {'Domain': "
        "'example.com', 'Username': 'johndoe', 'Token': "
        "'MDAxasdfY2F0aW9uIG1pY2hhZWxzYXNzZXIub3JnCjAwMTNpZGVudGlmaWVyIGtleQo"
        "wMDEwY2lkIGdlbiA9IDEKMDAyZGNpZCB1c2VyX2lkID0gQG1pY2hhZWw6bWljaGFlbHN"
        "hc3Nlci5vcmcKMDAxNmNpZCB0eXBlID0gYWNjZXNzCjAwMjFjaWQgbm9uY2UgPSB1cWJ"
        "2Tys1VlFyMUl3N0J1CjAwMmZzaWduYXR1cmUgeTBHhFmQrXiWjop8gQvg8I8ZuSHbEuI"
        "I8wp3YrAKEa4K'}, 'SSH': {'Address': 'matrix.example.com', 'Port': "
        "22, 'User': 'john'}}"
    )

    # Exercise
    actual: str = repr(toml)

    # Verify
    assert actual == desired

    # Cleanup - None


# vim: set ft=python :
