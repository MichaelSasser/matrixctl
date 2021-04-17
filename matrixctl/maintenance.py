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

"""Use this module to add the ``maintenance`` subcommand to ``matrixctl``."""

from __future__ import annotations

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction
from logging import debug

from .handlers.ansible import ansible_run
from .handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_maintenance(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl maintenance`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by
        ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "maintenance", help="Run maintenance tasks"
    )
    parser.set_defaults(func=maintenance)


def maintenance(_: Namespace) -> int:
    """Run the maintenance procedure of the ansible playbook.

    Parameters
    ----------
    _ : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.
        (In this case unused, but necessary because of the structure of the
        program).

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    debug("maintenance")

    toml: TOML = TOML()
    ansible_run(
        playbook=toml.get("ANSIBLE", "Playbook"),
        tags="run-postgres-vacuum,start",
    )

    return 0


# vim: set ft=python :
