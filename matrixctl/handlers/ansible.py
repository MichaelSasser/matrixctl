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

from logging import debug
from pathlib import Path
from typing import Dict
from typing import Optional

from ansible_runner.interface import Runner
from ansible_runner.runner_config import RunnerConfig


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


# ToDo: Make async to get debug output while running
def ansible_run(
    playbook: Path,
    tags: Optional[str] = None,
    extra_vars: Optional[Dict[str, str]] = None,
) -> None:
    runner_config: RunnerConfig = RunnerConfig(
        private_data_dir="/tmp",
        playbook=playbook,
        tags=tags,
        extravars=extra_vars,
    )
    runner_config.prepare()

    runner: Runner = Runner(config=runner_config)
    runner.run()

    # debugging output
    debug("Runner status")
    debug(f"{runner.status}: {runner.rc}")
    for host_event in runner.events:
        debug(host_event["event"])
    debug(f"Final status: {runner.stats}")


# vim: set ft=python :
