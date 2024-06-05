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

"""Use the functions of this module as helpers for passwords."""

from __future__ import annotations

import getpass
import logging
import sys


logger = logging.getLogger(__name__)


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


def create_user(user: str, admin: bool | None = None) -> str:
    """Ask the user to create a password.

    The user will be asked twice for a password. After
    that the function compares the two entered passwords. If they are the
    same, and not empty, the function will ask the user if the data is correct
    without disclosing the password.

    Parameters
    ----------
    user : str
        The username.
    admin : bool or none, default is None
        True, if the user will be an admin,
        False, if the user will not have eleveted permissions.
        None, if the admin permissions are not an criteria. The field will
        be omitted in the data.

    Returns
    -------
    password : str
        The user entered password.

    """
    try:
        passwd = ask_password()

        print("-" * 52)
        print("Please check, if the entered information is correct:")
        print(f"  Username: {user}")
        print("  Password: (REDACTED)")
        if admin is not None:
            print(f"  Admin:    {'yes' if admin else 'no'}")
        print("-" * 52)

        if ask_question():
            return passwd
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)


def ask_password() -> str:
    """Ask the user to create a password.

    The user will be asked twice for a password. After
    that the function compares the two entered passwords. If they are the
    same, and not empty, the function will return the password.

    Parameters
    ----------
    None

    Returns
    -------
    password : str
        The user entered password.

    """
    passwd: str | None = None
    passwd2: str | None = None

    while True:
        passwd = getpass.getpass()
        if not passwd:
            print("The password must not be empty!")
            continue
        passwd2 = getpass.getpass("Password (again): ")
        if passwd == passwd2:
            break
        print("The entered passwords do not match. Please try again!")

    return passwd


def ask_question(question: str = "Is everything correct?") -> bool:
    """Asks the user a simple yes/no a question.

    Notes
    -----
    - The user entered value is case-insensitive.
    - If the user answered with an invalid answer (not ``y`` / ``j`` / ``n``)
      the function asks again.

    Parameters
    ----------
    question : str
        The yes/no question the user should be asked

    Returns
    -------
    answer : bool
        ``True`` if the answer was ``y`` / ``j``, or
        ``False`` if the answer was ``n``

    """
    question += " [y/n]"

    while (answer := input(question).lower()) not in (
        "y",
        "j",
        "n",
    ):
        logger.info("User entered [y/n] pattern did not match")

    return answer in ("y", "j")


# vim: set ft=python :
