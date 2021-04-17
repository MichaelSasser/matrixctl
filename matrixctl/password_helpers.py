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

"""Use the functions of this module as helpers for passwords."""

from __future__ import annotations

import getpass
import secrets
import string

from logging import info
from typing import Optional


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


SPECIAL = "!§$%&/()=?.,;:_-#+*~{}[]°^@<>|\\"
ALPHABET = string.ascii_letters + string.digits + SPECIAL


def ask_password() -> Optional[str]:
    """Ask the user to create a password.

    The user will be asked twice, after
    that, the function compares the two entered passwords. If they are the
    same, the function will return the password.

    Notes
    -----
    If the user presses enter twice, without entering a password,
    the function will return ``None``. This is by-design.

    Parameters
    ----------
    None

    Returns
    -------
    password : str, optional
        The user entered password or ``None``, if the password does not match
        twice.

    """
    # ToDo: Check password (regex)
    passwd: str = "a"
    passwd2: str = "b"  # Something invalid: a==b is not True

    while passwd != passwd2:
        passwd = getpass.getpass()
        passwd2 = getpass.getpass("Password (again): ")

    return passwd if passwd == passwd2 else None


def gen_password(
    length: int = 16,
    min_digits: int = 3,
    min_special: int = 1,
    max_special: int = 3,
) -> str:
    """Generate a password.

    It uses lower- and uppercase
    characters, digits and some special characters, you can find in the
    ``SPECIAL`` variable in this file.

    It uses at least:

    - ``min_digits`` digits
    - ``min_special`` special characters

    It uses maximal:

    - ``max_special`` special characters

    The rest are lower- and uppercase characters.

    Parameters
    ----------
    length : int, defautl=16
        The desired length of the password to generate.
    min_digits : int, default=3
        The desired minimum of digits of the password.
    min_special : int, default=1
        The desired minimum of special characters of the password.
    max_special : int, default=3
        The desired maximum of special characters of the password.

    Returns
    -------
    password : str
        The generated password.

    """

    while True:
        password = "".join(secrets.choice(ALPHABET) for i in range(length))

        # pylint: disable=chained-comparison

        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= min_digits
            and min_special
            <= sum(c in SPECIAL for c in password)
            <= max_special
        ):
            return password


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
        info("User entered [y/n] pattern did not match")

    return answer in ("y", "j")


# vim: set ft=python :
