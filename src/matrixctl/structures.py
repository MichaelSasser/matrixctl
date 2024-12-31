# matrixctl
# Copyright (c) 2020-2023  Michael Sasser <Michael@MichaelSasser.org>
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

"""Use this module for structures."""

from __future__ import annotations

import typing as t


class Config(t.TypedDict):
    """Cast the YAML config to a typed dict."""

    servers: dict[str, ConfigServer]
    server: ConfigServer
    ui: ConfigUi


class ConfigServer(t.TypedDict):
    """Add a `server` to the YAML config structure."""

    ansible: ConfigServerAnsible
    synapse: ConfigServerSynapse
    api: ConfigServerAPI
    ssh: ConfigServerSSH
    maintenance: ConfigServerMaintenance


class ConfigServerAnsible(t.TypedDict):
    """Add `ansible` to `server` in the YAML config structure."""

    playbook: str


class ConfigServerSynapse(t.TypedDict):
    """Add `synapse` to `server` in the YAML config structure."""

    playbook: str


class ConfigServerAPI(t.TypedDict):
    """Add `api` to `server` in the YAML config structure."""

    domain: str
    username: str
    token: str
    concurrent_limit: int


class ConfigServerSSH(t.TypedDict):
    """Add `ssh` to `server` in the YAML config structure."""

    address: str
    port: int
    user: str


class ConfigServerMaintenance(t.TypedDict):
    """Add `maintenance` to `server` in the YAML config structure."""

    tasks: list[str]


class ConfigUi(t.TypedDict):
    """Add `Ui` to `server` in the YAML config structure."""

    image: ConfigUiImage


class ConfigUiImage(t.TypedDict):
    """Add `image` to `server` in the YAML config structure."""

    enabled: bool
    scale_factor: float  # Must be > 0.0
    max_height_of_terminal: float  # Must be > 0.0 and <= 1.0


# vim: set ft=python :
