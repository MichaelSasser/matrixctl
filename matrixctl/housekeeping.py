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
from logging import debug
from .ansible_handler import ansible_synapse

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def maintainance(_, cfg, __):
    debug(f"maintainance")
    ansible_synapse(
        ["--tags=run-postgres-synapse-janitor,run-postgres-vacuum,start"], cfg
    )


# vim: set ft=python :
