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
import string
import getpass
import secrets
from typing import Optional

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


SPECIAL = "!\"§$%&/()=?.,;:_-#'+*~{}[]`´°^@<>|\\"
ALPHABET = string.ascii_letters + string.digits + SPECIAL


def ask_password() -> Optional[str]:
    passwd: str = "a"
    passwd2: str = "b"

    while passwd != passwd2:
        passwd = getpass.getpass()
        passwd2 = getpass.getpass("Password (again): ")

    return passwd if passwd == passwd2 else None


def gen_password() -> str:
    while True:
        password = "".join(secrets.choice(ALPHABET) for i in range(16))

        # pylint: disable=chained-comparison

        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
            and 1 <= sum(c in SPECIAL for c in password) <= 3
        ):
            return password


def ask_question(question: str = "Is everything ok?") -> True:
    question += " [y/n]"

    while (answer := input(question).lower()) not in ("y", "j", "n",):  # noqa
        pass

    return answer in ("y", "j")


def adduser(arg, cfg, adminapi):
    """Adds a User to the synapse instance"""

    while True:
        passwd_generated: bool = False

        if arg.passwd is None:
            arg.passwd = ask_password()

        if arg.passwd == "":
            arg.passwd = gen_password()
            passwd_generated = True

        print(f"Username: {arg.user}")

        if passwd_generated:
            print(f"Password (generated): {arg.passwd}")
        else:
            print(f"Password: **HIDDEN**")
        print(f"Admin:    {'yes' if arg.admin else 'no'}")

        answer = ask_question()

        if answer:
            break
        arg.passwd = None

    if arg.ansible:
        ansible_synapse(
            [
                f"--extra-vars='username={arg.user} password={arg.passwd} admin={arg.admin}'",
                "--tags=register-user",
            ],
            cfg,
        )
    else:
        adminapi.adduser(arg.user, arg.passwd, arg.admin)


def deluser(arg, _, adminapi):
    adminapi.deluser(arg.user)


# vim: set ft=python :
