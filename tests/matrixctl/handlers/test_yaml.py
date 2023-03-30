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


def test_str(yaml: YAML) -> None:
    """Test __str__()."""

    # Setup
    desired: str = (
        "{'servers': {'default': {'ansible': {'playbook': '/path/to/ansible/"
        "playbook'}, 'synapse': {'playbook': '/path/to/synapse/playbook'}, '"
        "api': {'domain': 'example.com', 'username': 'johndoe', 'token': 'M"
        "DAxasdfY2F0aW9uIG1pY2hhZWxzYXNzZXIub3JnCjAwMTNpZGVudGlmaWVyIGtleQow"
        "MDEwY2lkIGdlbiA9IDEKMDAyZGNpZCB1c2VyX2lkID0gQG1pY2hhZWw6bWljaGFlbHN"
        "hc3Nlci5vcmcKMDAxNmNpZCB0eXBlID0gYWNjZXNzCjAwMjFjaWQgbm9uY2UgPSB1cW"
        "J2Tys1VlFyMUl3N0J1CjAwMmZzaWduYXR1cmUgeTBHhFmQrXiWjop8gQvg8I8ZuSHbE"
        "uII8wp3YrAKEa4K', 'concurrent_limit': 10}, 'ssh': {'address': 'matr"
        "ix.example.com', 'port': 22, 'user': 'john'}}}, 'server': {'ansible"
        "': {'playbook': '/path/to/ansible/playbook'}, 'synapse': {'playbook"
        "': '/path/to/synapse/playbook'}, 'api': {'domain': 'example.com', '"
        "username': 'johndoe', 'token': 'MDAxasdfY2F0aW9uIG1pY2hhZWxzYXNzZXI"
        "ub3JnCjAwMTNpZGVudGlmaWVyIGtleQowMDEwY2lkIGdlbiA9IDEKMDAyZGNpZCB1c2"
        "VyX2lkID0gQG1pY2hhZWw6bWljaGFlbHNhc3Nlci5vcmcKMDAxNmNpZCB0eXBlID0gY"
        "WNjZXNzCjAwMjFjaWQgbm9uY2UgPSB1cWJ2Tys1VlFyMUl3N0J1CjAwMmZzaWduYXR1"
        "cmUgeTBHhFmQrXiWjop8gQvg8I8ZuSHbEuII8wp3YrAKEa4K', 'concurrent_limi"
        "t': 10}, 'ssh': {'address': 'matrix.example.com', 'port': 22, 'user"
        "': 'john'}}}"
    )

    # Exercise
    actual: str = str(yaml)
    print(f'desired: str = "{actual}"')

    # Verify
    assert actual == desired

    # Cleanup - None


def test_repr(yaml: YAML) -> None:
    """Test __repr__()."""

    # Setup
    desired: str = (
        "{'servers': {'default': {'ansible': {'playbook': '/path/to/ansible/"
        "playbook'}, 'synapse': {'playbook': '/path/to/synapse/playbook'}, '"
        "api': {'domain': 'example.com', 'username': 'johndoe', 'token': 'M"
        "DAxasdfY2F0aW9uIG1pY2hhZWxzYXNzZXIub3JnCjAwMTNpZGVudGlmaWVyIGtleQow"
        "MDEwY2lkIGdlbiA9IDEKMDAyZGNpZCB1c2VyX2lkID0gQG1pY2hhZWw6bWljaGFlbHN"
        "hc3Nlci5vcmcKMDAxNmNpZCB0eXBlID0gYWNjZXNzCjAwMjFjaWQgbm9uY2UgPSB1cW"
        "J2Tys1VlFyMUl3N0J1CjAwMmZzaWduYXR1cmUgeTBHhFmQrXiWjop8gQvg8I8ZuSHbE"
        "uII8wp3YrAKEa4K', 'concurrent_limit': 10}, 'ssh': {'address': 'matr"
        "ix.example.com', 'port': 22, 'user': 'john'}}}, 'server': {'ansible"
        "': {'playbook': '/path/to/ansible/playbook'}, 'synapse': {'playbook"
        "': '/path/to/synapse/playbook'}, 'api': {'domain': 'example.com', '"
        "username': 'johndoe', 'token': 'MDAxasdfY2F0aW9uIG1pY2hhZWxzYXNzZXI"
        "ub3JnCjAwMTNpZGVudGlmaWVyIGtleQowMDEwY2lkIGdlbiA9IDEKMDAyZGNpZCB1c2"
        "VyX2lkID0gQG1pY2hhZWw6bWljaGFlbHNhc3Nlci5vcmcKMDAxNmNpZCB0eXBlID0gY"
        "WNjZXNzCjAwMjFjaWQgbm9uY2UgPSB1cWJ2Tys1VlFyMUl3N0J1CjAwMmZzaWduYXR1"
        "cmUgeTBHhFmQrXiWjop8gQvg8I8ZuSHbEuII8wp3YrAKEa4K', 'concurrent_limi"
        "t': 10}, 'ssh': {'address': 'matrix.example.com', 'port': 22, 'user"
        "': 'john'}}}"
    )

    # Exercise
    actual: str = repr(yaml)

    # Verify
    assert actual == desired

    # Cleanup - None


# vim: set ft=python :
