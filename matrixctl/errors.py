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

from sys import version_info
from typing import Any
from typing import Optional

from pkg_resources import get_distribution


class Error(Exception):
    BUGMSG: str = (
        "If you discover this message, please try updating "
        "MatrixCtl. If you see this message again, we would "
        "be glad, if you would run the same command again in debug-mode "
        '(matrixctl -d [...]) and hand in a "Bug report" at '
        "https://github.com/MichaelSasser/matrixctl/issues "
        "with the complete output.\n\n"
        f"Python version: {version_info.major}.{version_info.minor}."
        f"{version_info.micro} {version_info.releaselevel}\n"
        f"MatrixCtl version: {get_distribution('matrixctl').version} \n"
    )

    def __init__(
        self, message: Optional[str] = None, payload: Any = None
    ) -> None:  # pylint: disable=keyword-arg-before-vararg
        """Use this error like a normal error in your day-to-day programming.

        This is a commandline application. Therefor no user should ever see an
        error (except in debug-mode). This error informs the user that,
        getting a traceback is a bug in this application. It gives the person
        instructions, how to hand in a bug report, to contain them asap.
        """
        self.payload: Any = payload
        msg: str = self.__class__.BUGMSG

        if message:
            msg += "\nFor developers: " + message

        super().__init__(msg)


class ConfigFileError(Error):
    pass


class InternalResponseError(Error):
    pass


# vim: set ft=python :
