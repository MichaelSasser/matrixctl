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

# flake8: noqa
# pylint: disable:undefined-variable

from pathlib import Path
from pkg_resources import get_distribution


__version__ = get_distribution("matrixctl").version

HOME: str = str(Path.home())

# Don't mover these up
from .config_handler import *
from .ansible_handler import *
from .api_handler import *
from .git_handler import *
from .updating import *
from .housekeeping import *
from .account import *
from .provisioning import *

__all__ = (
    *config_handler.__all__,
    *ansible_handler.__all__,
    *api_handler.__all__,
    *git_handler.__all__,
    *updating.__all__,
    *housekeeping.__all__,
    *account.__all__,
    *provisioning.__all__,
)
