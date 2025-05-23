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
# pylint: disable:undefined-variable

"""Use MatrixCtl to control, manage, provision and deploy your homeserver."""

from __future__ import annotations

from pathlib import Path

from .package_version import get_version


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"
__version__: str = get_version(__name__, __file__) or "Unknown"


HOME: str = str(Path.home())


# vim: set ft=python :
