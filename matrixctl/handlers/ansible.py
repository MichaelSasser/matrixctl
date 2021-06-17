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

"""Run a ansible playbook with this module."""

from __future__ import annotations

import logging
import tempfile

from pathlib import Path

from ansible_runner.interface import Runner
from ansible_runner.runner_config import RunnerConfig


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

logger = logging.getLogger(__name__)


# ToDo: Make async to get debug output while running
def ansible_run(
    playbook: Path,
    tags: str | None = None,
    extra_vars: dict[str, str] | None = None,
) -> None:
    """Run an ansible playbook.

    Parameters
    ----------
    playbook : pathlib.Path
        The path to the ansible Playbook
    tags : str, optional
        The tags to use
    extra_vars : dict [str, str], optional
        The extra_vars to use.

    Returns
    -------
    None

    """
    with tempfile.TemporaryDirectory() as temp_dir:

        logger.debug(
            f'Created temporary directory "{temp_dir}" for the '
            "ansible-runner. The temporary directory will be removed after "
            "the ansible-runner succeeded or failed."
        )

        runner_config: RunnerConfig = RunnerConfig(
            private_data_dir=temp_dir,
            playbook=playbook,
            tags=tags,
            extravars=extra_vars,
        )
        runner_config.prepare()

        runner: Runner = Runner(config=runner_config)
        runner.run()

        # debug output
        logger.debug("Runner status")
        logger.debug(f"{runner.status}: {runner.rc}")
        for host_event in runner.events:
            logger.debug(host_event["event"])
        logger.debug(f"Final status: {runner.stats}")


# vim: set ft=python :
