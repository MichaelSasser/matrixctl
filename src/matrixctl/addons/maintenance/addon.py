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

"""Use this module to add the ``maintenance`` subcommand to ``matrixctl``."""

from __future__ import annotations

import logging

from argparse import Namespace
from collections.abc import Generator
from enum import Enum
from enum import unique

from matrixctl.handlers.ansible import ansible_run
from matrixctl.handlers.table import table
from matrixctl.handlers.yaml import YAML


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


logger = logging.getLogger(__name__)


@unique
class Task(Enum):
    """Use this enum for describing the maintenance task.

    Supported tasks:

    =============== ===================================================
    tasks           Description
    =============== ===================================================
    vacuum          Reclaims storage occupied by dead tuples.
    compress_state  Compress Synapse State Tables.
    =============== ===================================================

    """

    VACUUM = "run-postgres-vacuum"
    COMPRESS_STATE = "rust-synapse-compress-state"


def print_tasks() -> None:  # static data
    """Print a list of all available tasks."""
    table_generator: Generator[str, None, None] = table(
        [
            ["vacuum", "Reclaims storage occupied by dead tuples."],
            ["compress-state", "Compress Synapse State Tables."],
        ],
        ["Task", "Description"],
        sep=False,
    )
    for line in table_generator:
        print(line)


def addon(arg: Namespace, yaml: YAML) -> int:
    """Run the maintenance procedure of the ansible playbook.

    Parameters
    ----------
    arg : argparse.Namespace
        The ``Namespace`` object of argparse's ``parse_args()``.
    yaml : matrixctl.handlers.yaml.YAML
        The configuration file handler.

    Returns
    -------
    err_code : int
        Non-zero value indicates error code, or zero on success.

    """
    if arg.list:
        print_tasks()
        return 0

    todo = []
    for task in arg.tasks or yaml.get("server", "maintenance", "tasks"):
        # This loop can only contains a hand full of elements to go through

        try:
            todo.append(Task[task.replace("-", "_").upper()])
        except KeyError:  # task is not in enum
            logger.exception(
                (
                    'The task "%s" is not supported by MatrixCtl. '
                    "Below, you find a list of all available tasks."
                ),
                task,
            )
            print_tasks()
            return 1

    ansible_run(
        playbook=yaml.get("server", "ansible", "playbook"),
        tags=f"{','.join([t.value for t in todo])},start",
    )

    return 0


# vim: set ft=python :
