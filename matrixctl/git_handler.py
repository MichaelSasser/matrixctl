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
# import configparser
import datetime
from logging import debug

import git

from .config_handler import Config

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def git_pull(cnf: Config):
    # Get the last pulled datetime
    repo = git.Repo(cnf.ansible_path)

    assert not repo.bare
    heads = repo.heads
    master = heads.master

    log = master.log()
    last = datetime.datetime.fromtimestamp(log[-1].time[0])
    debug(f"Git: last update: {last}")

    # Pull request and "log" since last pulled
    g = git.cmd.Git(cnf.ansible_path)
    g.pull()
    print(
        g.log(
            f"--since={str(last)}",
            # f"--since={str(last.date())}",
            "--pretty=%as |%<(15) %an | %s",
        )
    )


# vim: set ft=python :
