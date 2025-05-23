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

"""Read and parse the configuration file with this module."""

from __future__ import annotations

import json
import logging
import os
import sys
import typing as t

from collections import ChainMap
from collections.abc import Iterable
from collections.abc import MutableMapping
from getpass import getuser
from pathlib import Path

import httpx

from jinja2 import Template
from jinja2 import Undefined
from ruamel.yaml import YAML as RuamelYAML  # noqa: N811
from ruamel.yaml.error import YAMLError

from matrixctl import __version__
from matrixctl.errors import ConfigFileError
from matrixctl.errors import ShouldNeverHappenError
from matrixctl.handlers.oidc import TokenManager
from matrixctl.structures import Config
from matrixctl.structures import ConfigServerAPI
from matrixctl.structures import ConfigServerAPIAuthOidc
from matrixctl.structures import ConfigUi
from matrixctl.structures import ConfigUiImage
from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


# Make sure the number of places of the source files line number does not
# change. Otherwise the debug output shifts.
def tree_printer(tree: t.Any, depth: int = 0) -> None:
    """Print the configuration file recursively.

    Parameters
    ----------
    tree : any
        Initial a ``matrixctl.typehints.Config`` and partials of it
        afterwards.
    depth : int
        The depth of the table

    Returns
    -------
    None

    """
    if not isinstance(tree, dict):
        msg: str = "There is something wrong with your config file."
        raise ConfigFileError(msg)
    for key in tree:
        if isinstance(tree[key], str | int | float | bool):
            logger.debug(
                "%s├─── %s: %s",
                "│ " * depth,
                key,
                secrets_filter(tree, key),
            )
        elif isinstance(tree[key], list | tuple):
            logger.debug(
                "%s├─── %s: [%s]",
                "│ " * depth,
                key,
                ", ".join(tree[key]),
            )
        else:
            logger.debug("%s├─┬─ %s:", "│ " * depth, key)
            tree_printer(tree[key], depth + 1)
    logger.debug("%s┴", "│ " * depth)


def secrets_filter(tree: dict[str, str], key: str) -> t.Any:
    """Redact secrets when printing the configuration file.

    Parameters
    ----------
    tree : dict [str, str]
        A patrial of ``tree`` from ``tree_printer``. (Can only be this type)
        afterwards.
    key : str
        A ``dict`` key. (Can only be this type)

    Returns
    -------
    None

    """
    redact = {"token", "synapse_password", "client_secret", "client_id"}
    return (
        f"<redacted length={len(tree[key])}>" if key in redact else tree[key]
    )


class JinjaUndefined(Undefined):  # type: ignore  # noqa: PGH003
    """Use this class as undefined argument in a Jinja2 Template.

    The class replaces every undefined template with an enpty string.

    """

    def __getattr__(self: JinjaUndefined, _: str) -> t.Any:
        """Return en empty string."""
        return ""


class YAML:
    """Use the YAML class to read and parse the configuration file(s)."""

    DEFAULT_PATHS: t.ClassVar[list[Path]] = [
        Path("/etc/matrixctl/config"),
        Path.home() / ".config/matrixctl/config",
    ]
    JINJA_PREDEFINED: t.ClassVar[dict[str, str | int]] = {
        "home": str(Path.home()),
        "user": getuser(),
        "default_ssh_port": 22,
        "default_api_concurrent_limit": 4,
        "well_knowen_path": ".well-known/openid-configuration",
    }
    __slots__ = ("__yaml", "api_auth_prepared", "server", "token_manager")

    def __init__(
        self: YAML,
        paths: Iterable[Path] | None = None,
        server: str | None = None,
    ) -> None:
        logger.debug("Loading Config file(s)")

        self.server: str = server or "default"

        self.__yaml: Config = self.get_server_config(
            paths or self.get_paths_to_config(),
            self.server,
        )
        self.token_manager: TokenManager | None = None
        self.api_auth_prepared: bool = False

        if not self.__yaml:  # dict is empty
            logger.error(
                "You need to create a configuration file for MatrixCtl. "
                "Make sure to check out the docs: https://matrixctl.rtfd.io/en"
                "/latest/getting_started/config_file.html",
            )
            # TODO: Remove the warning below before releasing v1.0.0.
            if int(__version__[0]) < 1:
                logger.error(
                    "Since MatixCtl v0.11.0 the configuration file uses the "
                    "yaml format. If you used MatrixCtl before, make sure to "
                    "update your config file to the yaml format.",
                )

        logger.debug("Config loaded for Server: %s", self.server)
        tree_printer(self.__yaml)

    @staticmethod
    def get_paths_to_config() -> tuple[Path, ...]:
        """Generate a tuple of path which may contain a configuration file.

        .. Note::

           This function preserves the order. The priority of the user
           configuration in ``XDG_CONFIG_HOME`` is higher than the global
           configuration in ``/etc/matrixctl/``. The priority of the
           file extension ``yaml`` is greater than the priority of the file
           extension ``yml``.

        .. Warning::

            The paths returned by this function might not exist.

        Returns
        -------
        config_paths : tuple of pathlib.Path
            A tuple of paths, which might contain a config file.

        """
        env_config_home: str | None = os.environ.get("XDG_CONFIG_HOME")
        paths: tuple[Path, ...] = (
            Path("/etc/matrixctl/config.yml"),
            Path("/etc/matrixctl/config.yaml"),
            (
                Path(env_config_home) / "matrixctl/config.yml"
                if env_config_home is not None
                else Path.home() / ".config/matrixctl/config.yml"
            ),
            (
                Path(env_config_home) / "matrixctl/config.yaml"
                if env_config_home is not None
                else Path.home() / ".config/matrixctl/config.yaml"
            ),
        )
        return tuple(sorted(paths, key=paths.index))  # unique, order preserved

    @staticmethod
    def read_from_file(yaml: RuamelYAML, path: Path) -> Config:
        """Read the config from a YAML file and render the Jinja2 tmplates.

        .. Note::

           - The Renderer does one pass. This means, you can only render
             templated strings but not the templated string of another
             templated string.
           - If the file was empty or does not exist, an empty dict will be
             returned.

        Parameters
        ----------
        yaml : ruamel.yaml.Yaml
            The yaml object.
        path : Path
            The path where the config file is located.

        Returns
        -------
        full_config : matrixctl.typehints.Config
            The full (with server name) config file as dict.

        """
        try:
            # The user should be able to use any file and location
            with path.open() as stream:
                template: Template = Template(
                    stream.read(),
                    undefined=JinjaUndefined,
                )
                rendered = YAML.JINJA_PREDEFINED | yaml.load(template.render())
                rendered["home"] = str(Path.home())
                # Override default return type t.Any with Config
                return t.cast("Config", yaml.load(template.render(rendered)))
        except YAMLError:
            logger.exception(
                (
                    "Please check your config file %s. MatrixCtl was "
                    "not able to read it."
                ),
                str(path),
            )
        except FileNotFoundError:
            logger.debug("The config file %s does not exist.", str(path))
        except IsADirectoryError:
            logger.exception(
                (
                    "The path to the configuration file you entered %s "
                    "seems to be a directory and not a "
                    "configuration file. Make sure the path is correct."
                ),
                str(path),
            )

        return t.cast("Config", {})

    @staticmethod
    def apply_defaults(config: Config, server: str) -> Config:
        """Apply defaults to the configuration.

        Parameters
        ----------
        config : matrixctl.structures.Config
            The configuration.

        server : str
            The selected server.

        Returns
        -------
        server : matrixctl.structures.Config
            The altered configuration.

        """

        #
        # Server
        #

        # Create api if it does not exist
        try:
            config["servers"][server]["api"]["concurrent_limit"]
        except KeyError:
            config["servers"][server]["api"] = t.cast("ConfigServerAPI", {})

        # Create default for concurrent_limit
        try:
            config["servers"][server]["api"]["concurrent_limit"]
        except KeyError:
            config["servers"][server]["api"]["concurrent_limit"] = 4

        # Auth type
        try:
            config["servers"][server]["api"]["auth_type"]
        except KeyError:
            config["servers"][server]["api"]["auth_type"] = "token"
        config["servers"][server]["api"]["auth_type"] = config["servers"][
            server
        ]["api"]["auth_type"].lower()

        # Create api.auth_oidc if it does not exist
        try:
            config["servers"][server]["api"]["auth_oidc"]["client_id"]
        except KeyError:
            config["servers"][server]["api"]["auth_oidc"] = t.cast(
                "ConfigServerAPIAuthOidc", {}
            )

        #
        # Ui
        #

        # Create ui if it does not exist
        try:
            config["ui"]["image"]
        except KeyError:
            config["ui"] = t.cast("ConfigUi", {})

        # Create ui if it does not exist
        try:
            config["ui"]["image"]["scale_factor"]
        except KeyError:
            config["ui"]["image"] = t.cast("ConfigUiImage", {})

        # Create default for display_scale_factor
        try:
            config["ui"]["image"]["scale_factor"]
        except KeyError:
            config["ui"]["image"]["scale_factor"] = 1.0

        # Create default for display_max_height_of_terminal
        try:
            config["ui"]["image"]["max_height_of_terminal"]
        except KeyError:
            config["ui"]["image"]["max_height_of_terminal"] = 0.33

        try:
            config["ui"]["image"]["enabled"]
        except KeyError:
            config["ui"]["image"]["enabled"] = False

        return config

    def get_server_config(
        self: YAML,
        paths: Iterable[Path],
        server: str,
    ) -> Config:
        """Read and concentrate the config in one dict.

        The ``servers: ...`` will be removed form the dict.
        A new entry ``server`` will be created, which represents the selected
        server.

        Notes
        -----
        When all files were empty or don't exist, an empty dict will be
        returned.

        Parameters
        ----------
        paths : Iterable of pathlib.Path
            The paths to the configfiles.
        server : str
            The selected server. (Default: "default")

        Returns
        -------
        server_config : matrixctl.typehints.Config
            The config for the selected server.

        """
        # RuamelYAML should not be part of the class.
        yaml: RuamelYAML = RuamelYAML(typ="safe")
        configs: t.Generator[Config, None, None] = (
            YAML.read_from_file(yaml, path) for path in paths
        )
        try:
            conf: Config = t.cast(
                "Config",
                dict(
                    ChainMap(
                        *(
                            t.cast(MutableMapping[t.Any, t.Any], config)  # noqa: TC006
                            for config in configs
                            if config
                        ),
                    ),
                ),
            )
            conf = self.apply_defaults(conf, server)
            conf["server"] = conf["servers"][server]

        except KeyError:
            logger.exception(
                "The server %s does not exist in your config file.",
                server,
            )
            sys.exit(1)
        except TypeError:
            logger.exception(
                (
                    "The Path(s) to the configuration file you entered %s "
                    "seems to have syntax paroblems. Make sure you use the "
                    "correct YAML syntax."
                ),
                paths,
            )
            sys.exit(1)
        return conf

    # TODO: doctest + fixture
    def get(self: YAML, *keys: str) -> t.Any:
        """Get a value from a config entry safely.

        **Usage**

        Pass strings, describing the path in the ``self.__yaml`` dictionary.
        Let's say, you are looking for the synapse path:

        Examples
        --------
        .. code-block:: python

           from matrixctl.handlers.yaml import YAML

           yaml: YAML = YAML()
           port: int = yaml.get("server", "ssh", "port")
           print(port)
           # Output: 22

        Parameters
        ----------
        *keys : str
            A tuple of strings describing the values you are looking for.

        Returns
        -------
        answer : any
            The value of the entry you described.

        """
        yaml_walker: t.Any = self.__yaml

        try:
            for key in keys:
                yaml_walker = yaml_walker[key]
        except KeyError:
            tree: str = ".".join(keys[:-1]).replace(
                "server",
                f"servers.{self.server}",
            )
            logger.exception(
                (
                    "Please check your config file. For this operation your "
                    "config file needs to have the entry %s in %s."
                ),
                keys[-1],
                tree,
            )
            sys.exit(1)

        if not isinstance(yaml_walker, dict):
            return yaml_walker

        # There is currently no scenario where a whole structure would be
        # beneficial.
        msg: str = (
            "The key you have asked for seems to be incorrect. "
            "Please make sure you ask for an single entry, "
            "not a entire section."
        )
        raise ConfigFileError(msg)

    @staticmethod
    def __get_oidc_config(issuer_url: str) -> JsonDict:
        """Retrieve OIDC provider configuration via discovery.

        Parameters
        ----------
        issuer_url : str
            Base URL of the OIDC issuer

        Returns
        -------
        dict[str, t.Any]
            OIDC provider configuration

        Raises
        ------
        httpx.HTTPStatusError
            For HTTP request failures
        ValueError
            If discovery document is invalid
        """
        try:
            discovery_url = issuer_url.rstrip("/")
            response = httpx.get(discovery_url, timeout=10)
            _ = response.raise_for_status()
            oidc_config: JsonDict = t.cast("JsonDict", response.json())
        except httpx.HTTPStatusError as e:
            logger.exception(
                "Discovery request failed: %s %s",
                e.response.status_code,
                e.response.text,
            )
            raise

        except json.JSONDecodeError:
            logger.exception(
                (
                    "The discovery request JSON response could not be "
                    "decoded. Invalid JSON: %s"
                ),
                response,
            )
            raise

        logger.debug("OIDC discovery response: %s", oidc_config)
        return oidc_config

    # TODO: Simplify. Maybe use get() instead of try/except?
    def ensure_api_auth(self) -> None:  # noqa: C901 PLR0915
        """Ensure the API authentication configuration is valid and prepared.

        This method checks the authentication type specified in the
        configuration and validates that all required fields for the selected
        authentication method are present. It supports 'token' and 'oidc'
        authentication types.

        For 'token' authentication, it verifies the presence of 'auth_token',
        'username', and 'token'. For 'oidc' authentication, it checks for
        required OIDC endpoints and credentials, and if necessary, fetches
        OIDC configuration from a discovery endpoint. It also initializes the
        TokenManager and retrieves claims and user information.

        Raises
        ------
        ConfigFileError
            If required configuration fields are missing or invalid.
        ValueError
            If the OIDC authorization endpoint is not found.
        """
        if self.api_auth_prepared:
            return
        # exists because it has a default value
        auth_type: str = self.__yaml["server"]["api"]["auth_type"]
        err_msg: str
        match auth_type:
            case "token":
                try:
                    self.__yaml["server"]["api"]["auth_token"]
                except KeyError as e:
                    err_msg = (
                        "You need to set the auth_token in your api config of "
                        "your config file if you use the token auth type."
                    )
                    raise ConfigFileError(err_msg) from e

                try:
                    self.__yaml["server"]["api"]["auth_token"]["username"]
                    self.__yaml["server"]["api"]["auth_token"]["token"]
                except KeyError as e:
                    err_msg = (
                        "When using the token auth type, you need to set "
                        "api.auth_token.username and api.auth_token.token in "
                        "the config file."
                    )
                    raise ConfigFileError(err_msg) from e
            case "oidc":
                # server.api.auth_oidc exisits because it has a default value

                # check if we need the server.api.auth_oidc.discovery_endpoint
                try:
                    self.__yaml["server"]["api"]["auth_oidc"]["token_endpoint"]
                    self.__yaml["server"]["api"]["auth_oidc"]["auth_endpoint"]
                    self.__yaml["server"]["api"]["auth_oidc"][
                        "userinfo_endpoint"
                    ]
                    self.__yaml["server"]["api"]["auth_oidc"]["jwks_uri"]
                except KeyError:
                    try:
                        discovery_endpoint: str = self.__yaml["server"]["api"][
                            "auth_oidc"
                        ]["discovery_endpoint"]
                        oidc_config: JsonDict = self.__get_oidc_config(
                            discovery_endpoint
                        )

                        self.__yaml["server"]["api"]["auth_oidc"][
                            "token_endpoint"
                        ] = t.cast("str", oidc_config["token_endpoint"])
                        self.__yaml["server"]["api"]["auth_oidc"][
                            "auth_endpoint"
                        ] = t.cast(
                            "str", oidc_config.get("authorization_endpoint")
                        )
                        self.__yaml["server"]["api"]["auth_oidc"][
                            "userinfo_endpoint"
                        ] = t.cast("str", oidc_config.get("userinfo_endpoint"))
                        self.__yaml["server"]["api"]["auth_oidc"][
                            "jwks_uri"
                        ] = t.cast("str", oidc_config.get("jwks_uri"))
                    except KeyError as e:
                        err_msg = (
                            "To use the oidc auth type, you need to set "
                            "either the api.auth_oidc.discovery_endpoint or "
                            "api.auth_oidc.token_endpoint, "
                            "api.auth_oidc.auth_endpoint, "
                            "api.auth_oidc.userinfo_endpoint and "
                            "api.auth_oidc.jwks_uri "
                        )
                        raise ConfigFileError(err_msg) from e

                    try:
                        self.__yaml["server"]["api"]["auth_oidc"]["client_id"]
                    except KeyError as e:
                        err_msg = (
                            "You need to set the client_id in your config "
                            "file, under api.auth_oidc.client_id, if you use "
                            "the oidc auth."
                        )
                        raise ConfigFileError(err_msg) from e
                    try:
                        self.__yaml["server"]["api"]["auth_oidc"][
                            "client_secret"
                        ]
                    except KeyError as e:
                        err_msg = (
                            "You need to set the client_secret in your config "
                            "file, under api.auth_oidc.client_secret, if you "
                            "use the oidc auth."
                        )
                        raise ConfigFileError(err_msg) from e

                    token_manager = TokenManager(
                        token_endpoint=self.__yaml["server"]["api"][
                            "auth_oidc"
                        ]["token_endpoint"],
                        client_id=self.__yaml["server"]["api"]["auth_oidc"][
                            "client_id"
                        ],
                        client_secret=self.__yaml["server"]["api"][
                            "auth_oidc"
                        ]["client_secret"],
                        auth_endpoint=self.__yaml["server"]["api"][
                            "auth_oidc"
                        ]["auth_endpoint"],
                        userinfo_endpoint=self.__yaml["server"]["api"][
                            "auth_oidc"
                        ]["userinfo_endpoint"],
                        jwks_uri=self.__yaml["server"]["api"]["auth_oidc"][
                            "jwks_uri"
                        ],
                    )

                    if not token_manager.auth_endpoint:
                        err_msg = (
                            "Authorization endpoint not found in OIDC "
                            "configuration"
                        )
                        raise ValueError(err_msg) from None

                    using_claims: set[str] = {
                        "openid",
                        "urn:synapse:admin:*",
                        "urn:matrix:org.matrix.msc2967.client:api:*",
                    }
                    _: str = token_manager.get_user_token(using_claims)
                    payload = token_manager.get_payload()
                    user_info = token_manager.get_user_info()

                    self.__yaml["server"]["api"]["auth_oidc"]["payload"] = (
                        payload
                    )
                    self.__yaml["server"]["api"]["auth_oidc"]["user_info"] = (
                        user_info
                    )
                    self.token_manager = token_manager
            case _:
                err_msg = (
                    f"Unknown auth type {auth_type} in your config file."
                    "Possible values are: 'token' and 'oidc'."
                )
                raise ConfigFileError(err_msg)
        self.api_auth_prepared = True

    def get_api_username(self) -> str:
        """Retrieve the API token for authentication.

        This method ensures API authentication is set up, then retrieves
        the username based on the configured authentication type. Supports
        'token' and 'oidc' auth types.

        Returns
        -------
        username : str
            The username.

        Raises
        ------
        ShouldNeverHappenError
            If the token manager is not initialized or the auth type is
            unknown.

        """
        self.ensure_api_auth()
        match self.get("server", "api", "auth_type"):
            case "token":
                return t.cast(
                    "str", self.get("server", "api", "auth_token", "username")
                )
            case "oidc":
                localpart = self.get(
                    "server", "api", "auth_oidc", "user_info", "username"
                )
                server = self.get("server", "api", "domain")
                return f"@{localpart}:{server}"
            case _:
                err_msg = "Unknown Username"
                raise ShouldNeverHappenError(err_msg)

    def get_api_token(self) -> str:
        """Retrieve the API token for authentication.

        This method ensures API authentication is set up, then retrieves
        the token based on the configured authentication type. Supports
        'token' and 'oidc' auth types.

        Returns
        -------
        token : str
            The API token string.

        Raises
        ------
        ShouldNeverHappenError
            If the token manager is not initialized or the auth type is
            unknown.

        """
        self.ensure_api_auth()
        match self.get("server", "api", "auth_type"):
            case "token":
                return t.cast(
                    "str", self.get("server", "api", "auth_token", "token")
                )
            case "oidc":
                using_claims: set[str] = {
                    "openid",
                    "urn:synapse:admin:*",
                    "urn:matrix:org.matrix.msc2967.client:api:*",
                }
                if not self.token_manager:
                    err_msg = (
                        "Token manager not initialized. "
                        "Call ensure_api_auth() first."
                    )
                    raise ShouldNeverHappenError(err_msg)
                return self.token_manager.get_user_token(using_claims)
            case _:
                err_msg = "Unknown Token"
                raise ShouldNeverHappenError(err_msg)

    def __repr__(self: YAML) -> str:
        """Wrap RuamelYAML repr."""
        return repr(self.__yaml)

    def __str__(self: YAML) -> str:
        """Wrap RuamelYAML str."""
        return str(self.__yaml)


# vim: set ft=python :
