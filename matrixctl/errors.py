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
from typing import Any
from sys import version_info
from pkg_resources import get_distribution


class Error(Exception):
    """Base class for exceptions in this module."""


class ConfigFileError(Error):
    pass


class BaseBugError(Error):
    BUGMSG: str = (
        "If you discover this message, please try updating "
        "MatricCtl. If you see this message again, we would "
        "be glad, if you would run the same command again in debug-mode "
        '(matrixctl -d [...]) and hand in a "Bug report" at '
        "https://github.com/MichaelSasser/matrixctl/issues "
        "with the complete output.\n"
        f"Python version: {version_info.major}.{version_info.minor}."
        f"{version_info.micro} {version_info.releaselevel}\n"
        f"ds2000 version: {get_distribution('matrixctl').version} \n"
    )

    def __init__(
        self, message: Any = None, *args, **kwargs
    ):  # pylint: disable=keyword-arg-before-vararg
        """Raised when an operation attempts a state, due to duck typing,
        that's not allowed and should be fixed asap.
        """
        msg = self.__class__.BUGMSG

        if message:
            msg += "\nFor developers: " + str(message)

        super().__init__(msg, *args, **kwargs)


class InternalResponseError(BaseBugError):
    pass


# vim: set ft=python :
