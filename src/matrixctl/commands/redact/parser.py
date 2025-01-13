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

"""Use this module to add the ``redact`` subcommand to ``matrixctl``."""

from __future__ import annotations

import typing as t

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import _SubParsersAction

from matrixctl.addon_manager import subparser


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


@subparser
def subparser_redact(subparsers: _SubParsersAction[t.Any]) -> None:
    """Create a subparser for the ``matrixctl redact`` command.

    Parameters
    ----------
    subparsers : argparse._SubParsersAction of typing.Any
        The object which is returned by
        ``parser.add_subparsers()``.

    Returns
    -------
    None

    """
    parser: ArgumentParser = subparsers.add_parser(
        "redact",
        help="Redact events",
        formatter_class=RawDescriptionHelpFormatter,
        description=(
            "This command allows an admin to redact the events of a given"
            " user. There are no restrictions on redactions for a local user."
            " By default, we puppet the user who sent the message to redact"
            " it themselves. Redactions for non-local users are issued using"
            " the admin user, and will fail in rooms where the admin user is"
            " not admin/does not have the specified power level to issue"
            " redactions."
        ),
    )
    parser.add_argument(
        "user_id",
        type=str,
        help=(
            "The fully qualified MXID of the user: for example,"
            ' "@user:server.com"'
        ),
    )
    parser.add_argument(
        "-r",
        "--room_ids",
        nargs="+",
        type=str,
        help=(
            "A list of rooms to redact the user's events in. If an empty list"
            "is provided all events in all rooms the user is a member of will"
            " be redacted"
        ),
    )
    parser.add_argument(
        "-t",
        "--reason",
        type=str,
        help=(
            'A Reason the redaction is being requested, ie "spam", "abuse", '
            "etc. This will be included in each redaction event, and be"
            " visible to users"
        ),
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=1000,
        help=(
            "A limit on the number of the user's events to search for ones"
            " that can be redacted (events are redacted newest to oldest)"
            " in each room, defaults to 1000 if not provided"
        ),
    )
    parser.set_defaults(addon="redact")


# vim: set ft=python :
