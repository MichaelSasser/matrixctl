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

"""Update and manage the synapse playbook repository with this module."""

from __future__ import annotations

import datetime
import sys

from logging import critical
from logging import debug
from logging import error
from logging import info
from pathlib import Path
from shutil import get_terminal_size
from textwrap import TextWrapper
from typing import List
from typing import Union

import git

from tabulate import tabulate


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


class Git:

    """Update and manage a repository."""

    def __init__(self, path: Union[Path, str]) -> None:
        self.path: Path = Path(path)
        self.repo = git.Repo(self.path)

        if self.repo.bare:
            critical(
                "Please make sure you entered the correct repository "
                "in [SYNAPSE] -> Playbook."
            )
            sys.exit(1)

        self.git = git.cmd.Git(self.path)
        self.heads = self.repo.heads
        self.master = self.heads.master

    @property
    def datetime_last_pulled_commit(self) -> datetime.datetime:
        """Get the datetime the commit was pulled last from git.

        This is used to determine which messages will be produced in the table.

        Parameters
        ----------
        None

        Returns
        -------
        datetime : datetime.datetime
            The datetime object.

        """
        log = self.master.log()

        return datetime.datetime.fromtimestamp(log[-1].time[0])

    def log(self, since: datetime.datetime | None = None) -> None:
        """Print a table of date, user and commit message since the last pull.

        Parameters
        ----------
        since : datetime.datetime, optional, default=None
            The datetime the last commit was puled.

        Returns
        -------
        None

        """
        cmd = ["--pretty=%as\t%an\t%s"]

        if since:
            cmd.append(f"--since={str(since)}")

        terminal_size_x, _ = get_terminal_size()
        debug(f"Terminal width = {terminal_size_x}")

        ######################################################################
        #                          Terminal width                            #
        #                          ^^^^^^^^^^^^^^                            #
        #                                                                    #
        # |<-------------------------------(121)-------------------------->| #
        # |<--------------------------(119)------------------------->|     | #
        # |<----------------------(34)--------------------->|        |     | #
        # |<------------------(32)----------------->|       |        |     | #
        # |<---------------(30)-------------->|     |       |        |     | #
        # |<-------------16------------>|     |     |       |        |     | #
        # |<---------14--------->|      |     |     |       |        |     | #
        # |<----12----->|        |      |     |     |       |        |     | #
        # |<--3-->|     |        |      |     |     |       |        |     | #
        # |_______d a t e________|______u s e r_____|_______commit_msg_____| #
        #                               |<--->|            |<------>|        #
        #                                 15                 x - 35          #
        #                                                                    #
        ######################################################################

        wrapper_user = TextWrapper(
            width=15, drop_whitespace=True, break_long_words=True
        )
        wrapper_comment = TextWrapper(
            width=terminal_size_x - 35,
            drop_whitespace=True,
            break_long_words=True,
        )

        log: List[List[str]] = [
            line.split("\t") for line in self.git.log(cmd).split("\n")
        ]

        if not log[0][0]:  # Nothing new
            info("Everything is up-to-date.")

            return

        for line in log:
            line[1] = wrapper_user.fill(text=line[1])
            line[2] = wrapper_comment.fill(text=line[2])

        print(
            tabulate(
                log,
                headers=("Date", "User", "Commit Message"),
                tablefmt="psql",
            )
        )

    def pull(self) -> None:
        """Git pull the latest commits from GH.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        # Get the last pulled datetime
        since = self.datetime_last_pulled_commit

        try:
            self.git.pull()
        except git.GitCommandError:
            error(
                "MatrixCtl was not able to connect to the synapse playbook "
                "on GitHub. Are you connected to the internet?"
            )
            sys.exit(1)

        self.log(since)


# vim: set ft=python :
