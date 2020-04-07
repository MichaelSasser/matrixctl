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
from tabulate import tabulate
from .ansible_handler import ansible_synapse
from .config_handler import Config

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


SPECIAL = "!\"§$%&/()=?.,;:_-#'+*~{}[]`´°^@<>|\\"
ALPHABET = string.ascii_letters + string.digits + SPECIAL


BOTS = {"whatsapp_", "whatsappbot", "telegram_", "telegrambot"}


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


def adduser(arg, cfg: Config, adminapi):
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


def deluser(arg, _: Config, adminapi):
    adminapi.deluser(arg.user)


def list_users(arg, cfg: Config, adminapi):
    len_domain = len(cfg.api_domain) + 1  # 1 for :
    from_user: int = 0
    users: list = []

    while True:
        lst = adminapi.list_users(from_user, show_guests=arg.guests).json()

        users += lst["users"]
        try:
            from_user = lst["next_token"]
        except KeyError:
            break

    user_list: list = []

    for user in users:
        name = user["name"][1:-len_domain]
        no_passwd_hash: bool = user["password_hash"] == ""
        deactivated: bool = bool(int(user["deactivated"]))
        admin: bool = bool(int(user["admin"]))
        guest: bool = bool(int(user["is_guest"]))

        # if no_bots and any([name.startswith(bot) for bot in BOTS]):
        #     continue

        if arg.no_bots and no_passwd_hash:
            continue

        user_list.append((name, deactivated, admin, guest,))
    print(
        tabulate(
            user_list,
            headers=("Name", "Deactivated", "Is Admin", "Is Guest"),
            tablefmt="psql",
        )
    )


# vim: set ft=python :
