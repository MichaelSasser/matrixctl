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

"""Use this module to add the ``stop`` subcommand to ``matrixctl``."""

from __future__ import annotations

from argparse import ArgumentParser
from argparse import Namespace
from argparse import _SubParsersAction as SubParsersAction

from .handlers.ansible import ansible_run
from .handlers.toml import TOML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def subparser_stop(subparsers: SubParsersAction) -> None:
    """Create a subparser for the ``matrixctl stop`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction
        The object which is returned by ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "stop", help="Stops all OCI containers"
    )
    parser.set_defaults(func=stop)


def stop(_: Namespace) -> int:
    """Stop the OCI containers.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    toml: TOML = TOML()
    ansible_run(toml.get("ANSIBLE", "Playbook"), tags="stop")
    return 0


# vim: set ft=python :
