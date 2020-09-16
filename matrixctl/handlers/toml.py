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
from __future__ import annotations

import sys
import warnings

from copy import deepcopy
from logging import debug
from logging import error
from pathlib import Path
from types import TracebackType
from typing import Any
from typing import Dict
from typing import ItemsView
from typing import Iterator
from typing import KeysView
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from typing import ValuesView

import toml

from matrixctl.errors import ConfigFileError


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class TOML:
    def __init__(self, path: Optional[Path] = None) -> None:
        debug("Loading Config file(s)")

        if path is None:
            self.__default: bool = True

        default_config: List[str] = [
            "/etc/matrixctl/config",
            str(Path.home() / ".config/matrixctl/config"),
        ]
        # self.__check_paths(self.__class__.FILE_PATH)

        # with warnings.catch_warnings():
        #     captureWarnings(True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                # toml.load is a MutableMapping
                self.__toml: Dict[str, Any] = deepcopy(
                    dict(
                        toml.load(
                            default_config if self.__default else str(path)
                        )
                    )
                )
            except FileNotFoundError:
                error(
                    "To use this program you need to have a config file in"
                    '/etc/matrixctl/config" or in '
                    '"~/.config/matrixctl/config".'
                )
                sys.exit(1)
            except TypeError:
                raise ConfigFileError()
            except toml.TomlDecodeError:
                error(
                    "Please check your config file. MatrixCtl was not able "
                    "to read it."
                )
                sys.exit(1)

        self.__debug_output()

    def __debug_output(self) -> None:
        for key in self.__toml:
            debug(f"[{key}]")

            for entry in self.__toml[key]:
                if entry == "Token":
                    length = len(self.__toml[key][entry])
                    debug(f"  ├─  {entry} := **HIDDEN (Length={length})**")
                else:
                    debug(f"  ├─  {entry} := {self.__toml[key][entry]}")
            debug("  ┴")

    def get(
        self,
        keys: Union[List[str], Tuple[str, ...]],
        none_on_error: bool = False,
    ) -> Any:
        """Get a value from a config entry safely.

        This is the only way, the config is asked for a value from an entry.
        The other methods are used for non MatrixCtl TOML files.

        **Usage**

        Pass in a list or tuple with strings describing the path in the
        ``self.__toml`` dictionary.
        Let's say, you are looking for the synapse path:

        >>> toml.get(("SYNAPSE", "Path"))
        '/home/dwight/SomRandomDirectory/synapse'

        :param keys:  A string or tuple describing the values you are looking
                      for.
        :return:      The value of the entry you described.
        """
        toml_walker: Union[Dict[str, Any], Any] = self.__toml

        try:
            for key in keys:
                toml_walker = toml_walker.__getitem__(key)
        except KeyError:
            if none_on_error:
                return None
            error(
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

    def has_key(self, key: str) -> bool:
        return key in self.__toml

    def keys(self) -> KeysView[str]:
        return self.__toml.keys()

    def values(self) -> ValuesView[Any]:
        return self.__toml.values()

    def items(self) -> ItemsView[str, Any]:
        return self.__toml.items()

    def copy(self) -> Dict[str, str]:
        return self.__toml.copy()

    def __getitem__(self, key: str) -> Any:
        return self.__toml[key]

    def __len__(self) -> int:
        return len(self.__toml)

    def __contains__(self, item: str) -> bool:
        return item in self.__toml

    def __iter__(self) -> Iterator[str]:
        return iter(self.__toml)

    def __enter__(self) -> TOML:
        """Use the class with the ``with`` statement`` statement.

        This is currently not really needed, but unifies the way handlers are
        used.
        """

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Use the class with the ``with`` statement`` statement.

        This is currently not really needed, but unifies the way handlers are
        used.
        """

        return

    def __repr__(self) -> str:
        return repr(self.__toml)

    def __str__(self) -> str:
        return str(self.__toml)


#
# vim: set ft=python :
