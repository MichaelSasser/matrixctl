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

import getpass
import secrets
import string

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

    .. note:: If the user presses enter twice, without entering a password,
              the function will return ``None``. This is by-design.

    :return: Returns the user entered password or ``None``
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

    :param length:       The desired length of the password to generate
    :param min_digits:   The desired minimum of digits of the password
    :param min_special:  The desired minimum of special characters of the
                         password
    :param max_special:  The desired maximum of special characters of the
                         password
    :return:             It returns the generated password
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

    The answer will be returned as ``bool``.
    - ``True``: if the user answered ``y`` / ``j`` (j for the German yes: Ja)
    - ``False``: if the user answers ``n``

    If the user answerd with an invalid answer (not ``y`` / ``j`` / ``n``)
    the function asks again.

    :param question:  The yes/no question the user should be asked
    :return:          ``True`` if the answer was ``y`` / ``j`` and ``False``
                      if the answer was ``n``
    """
    question += " [y/n]"

    while (answer := input(question).lower()) not in (
        "y",
        "j",
        "n",
    ):  # noqa
        pass

    return answer in ("y", "j")


# vim: set ft=python :
