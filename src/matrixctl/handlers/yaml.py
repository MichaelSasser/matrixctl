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

import logging
import os
import sys
import typing as t

from collections import ChainMap
from collections.abc import Iterable
from collections.abc import MutableMapping
from getpass import getuser
from pathlib import Path

from jinja2 import Template
from jinja2 import Undefined
from ruamel.yaml import YAML as RuamelYAML  # noqa: N811
from ruamel.yaml.error import YAMLError

from matrixctl import __version__
from matrixctl.errors import ConfigFileError
from matrixctl.structures import Config
from matrixctl.structures import ConfigServer
from matrixctl.structures import ConfigServerAPI


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
    redact = {"token", "synapse_password"}
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
    }
    __slots__ = ("__yaml", "server")

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
                return t.cast(Config, yaml.load(template.render(rendered)))
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

        return t.cast(Config, {})

    @staticmethod
    def apply_defaults(server: ConfigServer) -> ConfigServer:
        """Apply defaults to the configuration.

        Parameters
        ----------
        server : matrixctl.structures.ConfigServer
            The configuration of a (home)server.

        Returns
        -------
        server : matrixctl.structures.ConfigServer
            The configuration of a (home)server with applied defaults.

        """
        # Create api if it does not exist
        try:
            server["api"]["concurrent_limit"]
        except KeyError:
            server["api"] = t.cast(ConfigServerAPI, {})

        # Create default for concurrent_limit
        try:
            server["api"]["concurrent_limit"]
        except KeyError:
            server["api"]["concurrent_limit"] = 4

        return server

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
                Config,
                dict(
                    ChainMap(
                        *(
                            t.cast(MutableMapping[t.Any, t.Any], config)
                            for config in configs
                            if config
                        ),
                    ),
                ),
            )
            conf["server"] = self.apply_defaults(conf["servers"][server])

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

    def __repr__(self: YAML) -> str:
        """Wrap RuamelYAML repr."""
        return repr(self.__yaml)

    def __str__(self: YAML) -> str:
        """Wrap RuamelYAML str."""
        return str(self.__yaml)


# vim: set ft=python :
