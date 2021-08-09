#!/usr/bin/env python
# matrixctl
# Copyright (c) 2020  Michael Sasser <Michael@MichaelSasser.org>
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

from collections import ChainMap
from collections.abc import Generator
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from typing import cast

from ruamel.yaml import YAML as RuamelYAML
from ruamel.yaml.error import YAMLError

from matrixctl import __version__
from matrixctl.errors import ConfigFileError
from matrixctl.typehints import YAMLFullConfigType  # cast
from matrixctl.typehints import YAMLServerConfigType


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


class YAML:

    """Use the YAML class to read and parse the configuration file(s)."""

    DEFAULT_PATHS: list[Path] = [
        Path("/etc/matrixctl/config"),
        Path.home() / ".config/matrixctl/config",
    ]
    __slots__ = ("__yaml", "server")

    def __init__(
        self, paths: Iterable[Path] | None = None, server: str = "default"
    ) -> None:
        logger.debug("Loading Config file(s)")

        self.server: str = server

        self.__yaml: YAMLServerConfigType = self.get_server_config(
            paths or self.get_paths_to_config(), server
        )

        if not self.__yaml:  # dict is empty
            logger.error(
                "You need to create a configuration file for MatrixCtl. "
                "Make sure to check out the docs: https://matrixctl.rtfd.io/en"
                "/latest/getting_started/config_file.html"
            )
            # TODO: Remove the warning below before releasing v1.0.0.
            if int(__version__[0]) < 1:
                logger.error(
                    "Since MatixCtl v0.11.0 the configuration file uses the "
                    "yaml format. If you used MatrixCtl before, make sure to "
                    "update your config file to the yaml format."
                )

        self.__debug_output()

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
    def read_from_file(yaml: RuamelYAML, path: Path) -> YAMLFullConfigType:
        """Read the configuration from a YAML file.

        .. Note::

           If the file was empty or does not exist, an empty dict will be
           returned.

        Parameters
        ----------
        yaml : ruamel.yaml.Yaml
            The yaml object.
        path : Path
            The path where the config file is located.

        Returns
        -------
        full_config : matrixctl.typehints.YAMLFullConfigType
            The full (with server name) config file as dict.

        """
        try:
            with open(path) as stream:
                # Override default return type Any with YAMLFullConfigType
                return cast(YAMLFullConfigType, yaml.load(stream))
        except YAMLError:
            logger.error(
                f"Please check your config file {str(path)}. MatrixCtl was "
                "not able to read it."
            )
        except FileNotFoundError:
            logger.debug(f'The config file "{str(path)}" does not exist.')
        except IsADirectoryError:
            logger.error(
                "The path to the configuration file you entered "
                f'"{str(path)}" seems to be a directory and not a '
                "configuration file. Make sure the path is correct."
            )

        return {}

    @staticmethod
    def get_server_config(
        paths: Iterable[Path],
        server: str | None = None,
    ) -> YAMLServerConfigType:
        """Read and concentrate the config in one dict.

        .. Note::

           When all files were empty or don't exist, an empty dict will be
           returned.

        Parameters
        ----------
        paths : Iterable of pathlib.Path
            The paths to the configfiles.
        server : str
            The selected server. (Defautl: "default")

        Returns
        -------
        server_config : matrixctl.typehints.YAMLServerConfigType
            The config for the selected server.

        """
        # RuamelYAML should not be part of the class.
        yaml: RuamelYAML = RuamelYAML(typ="safe")
        configs: Generator[YAMLFullConfigType, None, None] = (
            YAML.read_from_file(yaml, path) for path in paths
        )
        try:
            return dict(ChainMap(*(config for config in configs if config)))[
                server or "default"
            ]
        except KeyError:
            logger.error(
                f'The server "{server}" does not exist in your config file.'
            )
            sys.exit(1)
        except TypeError:
            logger.error(
                f'The Path(s) to the configuration file you entered "{paths}" '
                "seems to have syntax paroblems. Make sure you use the "
                "correct YAML syntax."
            )
            sys.exit(1)

    def __debug_output(self) -> None:
        """Create a debug output for the YAML file.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        logger.debug(f'Config loaded for Server: "{self.server}"')
        for key in self.__yaml:
            logger.debug(f"{key}:")

            for entry in self.__yaml[key]:
                if entry == "token":
                    length = len(self.__yaml[key][entry])
                    logger.debug(
                        f"  ├─  {entry} : **REDACTED (Length={length})**"
                    )
                else:
                    logger.debug(f"  ├─  {entry} := {self.__yaml[key][entry]}")
            logger.debug("  ┴")

    # TODO: doctest + fixture
    def get(self, *keys: str) -> Any:
        """Get a value from a config entry safely.

        **Usage**

        Pass strings, describing the path in the ``self.__yaml`` dictionary.
        Let's say, you are looking for the synapse path:

        Examples
        --------
        .. code-block:: python

           from matrixctl.handlers.yaml import YAML

           yaml: YAML = YAML()
           port: int = yaml.get("ssh", "port")
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
        yaml_walker: dict[str, Any] | Any = self.__yaml

        try:
            for key in keys:
                yaml_walker = yaml_walker.__getitem__(key)
        except KeyError:
            logger.error(
                "Please check your config file. For this operation your "
                f'config file needs to have the entry "{keys[-1]}" '
                f'in "{keys[0]}".'
            )
            sys.exit(1)

        if not isinstance(yaml_walker, dict):
            return yaml_walker
        raise ConfigFileError(
            "The key you have asked for seems to be incorrect. "
            "Please make sure you ask for an single entry, "
            "not a entire section."
        )

    def __repr__(self) -> str:
        return repr(self.__yaml)

    def __str__(self) -> str:
        return str(self.__yaml)


# vim: set ft=python :
