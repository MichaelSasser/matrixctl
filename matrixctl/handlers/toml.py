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
import sys
import warnings

from copy import deepcopy
from pathlib import Path
from typing import Any
from typing import cast

import toml

from matrixctl.errors import ConfigFileError


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


class TOML:

    """Use the TOML class to read and parse the configuration file(s)."""

    DEFAULT_PATHS: list[Path] = [
        Path("/etc/matrixctl/config"),
        Path.home() / ".config/matrixctl/config",
    ]
    __instance: TOML | None = None
    __slots__ = ("__toml",)

    def __init__(self, path: Path | None = None) -> None:
        logger.debug("Loading Config file(s)")

        paths: list[Path] = []
        if path is None:
            paths += self.__class__.DEFAULT_PATHS

        self.__toml: dict[str, Any] = self.__open(paths)

        self.__debug_output()

    def __new__(cls) -> TOML:  # TODO: weakref
        """Make TOML a Singelton.

        Parameters
        ----------
        cls : matrixctl.handlers.TOML
            New instance.

        Returns
        -------
        toml_instance : TOML
            A new or reused (Singelton) TOML instance.

        """
        if cls.__instance is None:
            logger.debug("Creating new TOML instance.")
            cls.__instance = cast(TOML, super().__new__(cls))
        return cls.__instance

    @staticmethod
    def __open(paths: list[Path]) -> dict[str, Any]:
        """Open a TOML file and suppress warnings of the toml module.

        Parameters
        ----------
        paths : list of pathlib.Path
            A list of paths to check for the configuration files (toml) to
            combine into one config, which can be used by MatrixCtl.

        Returns
        -------
        toml : dict [str, any]
            The toml file structure represented as dict.

        """
        config_files: list[str] = [str(path) for path in paths]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                # toml.load is a MutableMapping
                # Only lists, tuples are not supported.
                return deepcopy(dict(toml.load(config_files)))
            except FileNotFoundError:
                logger.error(
                    "To use this program you need to have a config file in"
                    '/etc/matrixctl/config" or in '
                    '"~/.config/matrixctl/config".'
                )
                sys.exit(1)
            except TypeError as e:
                raise ConfigFileError from e
            except toml.TomlDecodeError:
                logger.error(
                    "Please check your config file. MatrixCtl was not able "
                    "to read it."
                )
                sys.exit(1)

    def __debug_output(self) -> None:
        """Create a debug output for the TOML file.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        for key in self.__toml:
            logger.debug(f"[{key}]")

            for entry in self.__toml[key]:
                if entry == "Token":
                    length = len(self.__toml[key][entry])
                    logger.debug(
                        f"  ├─  {entry} := **HIDDEN (Length={length})**"
                    )
                else:
                    logger.debug(f"  ├─  {entry} := {self.__toml[key][entry]}")
            logger.debug("  ┴")

    # TODO: doctest + fixture
    def get(self, *keys: str) -> Any:
        """Get a value from a config entry safely.

        **Usage**

        Pass strings, describing the path in the ``self.__toml`` dictionary.
        Let's say, you are looking for the synapse path:

        Examples
        --------
        .. code-block:: python

           from matrixctl.handlers.toml import TOML

           toml: TOML = TOML()
           port: int = toml.get("SSH", "Port")
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
        toml_walker: dict[str, Any] | Any = self.__toml

        try:
            for key in keys:
                toml_walker = toml_walker.__getitem__(key)
        except KeyError:
            logger.error(
                "Please check your config file. For this operation your "
                f'config file needs to have the entry "{keys[-1]}" '
                f'In the section "[{keys[0]}]".'
            )
            sys.exit(1)

        if not isinstance(toml_walker, dict):
            return toml_walker
        raise ConfigFileError(
            "The key you have asked for seems to be incorrect. "
            "Please make sure you ask for an single entry, "
            "not a entire section."
        )

    def __repr__(self) -> str:
        return repr(self.__toml)

    def __str__(self) -> str:
        return str(self.__toml)


#
# vim: set ft=python :
