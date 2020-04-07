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
import sys
import configparser
import functools

from typing import Tuple
from pathlib import Path
from logging import debug, fatal

from matrixctl import HOME

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class ConfigFileError(Exception):
    pass


def error_if_not_available(method):
    """A wrapper, that checks, if the configuration is available and returns
    it. If the information is not available. it throws an error.
    """

    @functools.wraps(method)
    def wrapper_error_if_not_available(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except (KeyError, TypeError):
            fatal(
                f"Please check your config file: "
                f"{str(method.__name__).split('_')[0].upper()} "
                f"({str(method.__name__).split('_')[1]} entry)"
            )
            sys.exit(1)

    return wrapper_error_if_not_available


def none_if_not_available(method):
    """A wrapper, that checks, if the configuration is available and returns
    it. If the information is not available. it returns None.
    """

    @functools.wraps(method)
    def wrapper_none_if_not_available(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except (KeyError, TypeError):
            debug(f"Config entry not available for: {method.__name__}")

            return None

    return wrapper_none_if_not_available


# ToDo: Is the token length always the same? should be. If yes: check token
# length to prevent copy error.
class Config:
    FILE_PATH: Tuple[Path] = (
        Path("/etc/matrixctl/config"),
        Path(f"/{HOME}/.config/matrixctl/config"),
    )

    def __init__(self):
        debug("Loading Config file(s)")

        self.__check_path(self.__class__.FILE_PATH)

        self.config = configparser.ConfigParser()
        self.config.read(self.__class__.FILE_PATH)

        # Debugging
        self.__debug_output()

        # [ANSIBLE]
        try:
            self.config_ansible = self.config["ANSIBLE"]
        except KeyError:
            raise ConfigFileError(
                "Please check your configuration file. "
                "The [DEFAULT] section is mandatory."
            )
        except TypeError:
            raise ConfigFileError(
                "To use this program you need to have a config file in"
                '/etc/matrixctl/config" or in "~/.config/matrixctl/config".'
            )

        # [API]
        try:
            self.config_api = self.config["API"]
        except KeyError:
            self.config_api = None

        # [SERVER]
        try:
            self.config_server = self.config["SERVER"]
        except KeyError:
            self.config_server = None

    def __debug_output(self):
        for section in self.config.sections():
            debug(f"[{section}]")

            for entry in self.config[section]:
                if entry == "token":
                    length = len(self.config[section][entry])
                    debug(f"  ├─  {entry} := **HIDDEN (Length={length})**")
                else:
                    debug(f"  ├─  {entry} := {self.config[section][entry]}")
            debug("  ┴")

    @staticmethod
    def __check_path(file_path):
        path_exists: bool = False

        for p in file_path:
            if p.exists():
                path_exists = True

        if not path_exists:
            fatal(
                "To use this program you need to have a config file in "
                '/etc/matrixctl/config" or in "~/.config/matrixctl/config".'
            )
            sys.exit(1)

    @property
    def ansible_path(self) -> Path:
        return Path(self.config_ansible["MatrixDockerAnsibleDeployPath"])

    @property
    @error_if_not_available
    def api_token(self) -> str:
        return self.config_api["Token"]

    @property
    @error_if_not_available
    def api_domain(self) -> str:
        return self.config_api["Domain"]

    @property
    @none_if_not_available
    def server_cfg(self) -> str:
        return self.config_server["AnsibleCfg"]

    @property
    @none_if_not_available
    def server_play(self) -> str:
        return self.config_server["AnsiblePlaybook"]

    @property
    @none_if_not_available
    def server_tags(self) -> str:
        return self.config_server["AnsibleTags"]


# vim: set ft=python :
