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

from matrixctl.typehints import JsonDict


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
    alias: ConfigServerAlias


class ConfigServerAlias(t.TypedDict):
    """Add a `alias` to `server` in the YAML config structure."""

    room: tuple[ConfigServerAliasRoom, ...]


class ConfigServerAliasRoom(t.TypedDict):
    """Add a `room` to `server.alias` in the YAML config structure."""

    name: str
    room_id: str


class ConfigServerAnsible(t.TypedDict):
    """Add `ansible` to `server` in the YAML config structure."""

    playbook: str


class ConfigServerSynapse(t.TypedDict):
    """Add `synapse` to `server` in the YAML config structure."""

    playbook: str


class ConfigServerAPI(t.TypedDict):
    """Add `api` to `server` in the YAML config structure."""

    domain: str
    auth_type: str
    auth_token: ConfigServerAPIAuthToken
    auth_oidc: ConfigServerAPIAuthOidc
    concurrent_limit: int


class ConfigServerAPIAuthToken(t.TypedDict):
    """Add `auth_token` to `server.api` in the YAML config structure."""

    username: str
    token: str


class ConfigServerAPIAuthOidc(t.TypedDict):
    """Add `auth_oidc` to `server.api` in the YAML config structure."""

    discovery_endpoint: str
    client_id: str
    client_secret: str
    token_endpoint: str
    auth_endpoint: str
    userinfo_endpoint: str
    jwks_uri: str
    claims: t.Iterable[str]

    # Dynamically generated. Any user input will be overwritten.
    user_info: JsonDict
    payload: JsonDict


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
