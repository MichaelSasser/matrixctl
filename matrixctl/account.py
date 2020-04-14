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
import sys
import string
import getpass
import secrets
import datetime
from typing import Optional, List, Tuple, Any, Dict
from argparse import Namespace
from logging import debug, error
from tabulate import tabulate
from .ansible_handler import ansible_synapse
from .config_handler import Config
from .api_handler import Api
from .ssh_handler import Ssh
from .typing import JsonDict

__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"


SPECIAL = "!§$%&/()=?.,;:_-#+*~{}[]°^@<>|\\"
ALPHABET = string.ascii_letters + string.digits + SPECIAL


BOTS = {"whatsapp_", "whatsappbot", "telegram_", "telegrambot"}


def ask_password() -> Optional[str]:
    """Ask the user to create a password. The user will be asked twice, after
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
    """This function generates a password. It uses lower- and uppercase
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
    """This function asks the user for a simple yes/no a question and returns
    the answer as ``bool``:

    - ``True``: if the user answered ``y`` / ``j`` (j for the German yes: Ja)
    - ``False``: if the user answers ``n``

    If the user answerd with an invalid answer (not ``y`` / ``j`` / ``n``)
    the function asks again.

    :param question:  The yes/no question the user should be asked
    :return:          ``True`` if the answer was ``y`` / ``j`` and ``False``
                      if the answer was ``n``
    """
    question += " [y/n]"

    while (answer := input(question).lower()) not in ("y", "j", "n",):  # noqa
        pass

    return answer in ("y", "j")


def adduser(arg: Namespace, cfg: Config) -> None:
    """Adds a User to the synapse instance. It runs ``ask_password()``
    first. If ``ask_password()`` returns ``None`` it generates a password
    with ``gen_password()``. Then it gives the user a overview of the
    username, password and if the new user should be generated as admin
    (if you added the ``--admin`` argument). Next, it asks a question,
    if the entered values are correct with the ``ask_question`` function.

    If the ``ask_question`` function returns True, it continues. If not, it
    starts from the beginning.

    Depending on the ``--ansible`` switch it runs the ``adduser`` command
    via ansible or the API

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param cfg:       The ``Config`` class
    :return:          None
    """

    with Api(cfg.api_domain, cfg.api_token) as api:
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
            arg.admin = "yes" if arg.admin else "no"
            ansible_synapse(
                [
                    "--tags=register-user",
                    "--extra-vars",
                    f'{{"username":"{arg.user}","password":"{arg.passwd}","admin":"{arg.admin}"}}',
                ],
                cfg.ansible_path,
            )
        else:
            api.adduser(arg.user, arg.passwd, arg.admin)


def adduser_jitsi(arg: Namespace, cfg: Config) -> None:
    """Adds a User to the jitsi instance. It runs ``ask_password()``
    first. If ``ask_password()`` returns ``None`` it generates a password
    with ``gen_password()``. Then it gives the user a overview of the
    username, password and if the new user should be generated as admin
    (if you added the ``--admin`` argument). Next, it asks a question,
    if the entered values are correct with the ``ask_question`` function.

    If the ``ask_question`` function returns True, it continues. If not, it
    starts from the beginning.

    It runs the ``adduser`` method of the ``Ssh`` class.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param cfg:       The ``Config`` class
    :return:          None
    """

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

        answer = ask_question()

        if answer:
            break
        arg.passwd = None

    with Ssh(cfg) as ssh:
        ssh.adduser(arg.user, arg.passwd)


def deluser(arg: Namespace, cfg: Config) -> None:
    """This function deletes a user from the matrix instance.
    It uses the synapse admin API.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param _:         Not used (The ``Config`` class)
    :return:          None
    """
    with Api(cfg.api_domain, cfg.api_token) as api:
        api.deluser(arg.user)


def deluser_jitsi(arg: Namespace, cfg: Config) -> None:
    """This function deletes a user from the jitsi instance.
    It uses the ``Ssh`` class from the ``ssh_handler``.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param cfg:       The ``Config`` class
    :return:          None
    """
    with Ssh(cfg) as ssh:
        ssh.deluser(arg.user)


def users(arg: Namespace, cfg: Config) -> None:
    """This function generates and prints a table of matrix user accounts.
    The table can be modified with:

    - the ``--guests`` switch: ``args.guests`` is True, else ``False``
    - the ``--no-bots`` switch: ``args.no_bots`` is True, else ``False``

    If you don't want any bots in the table use the ``--no-bots`` switch.
    If you want guests in the table use the ``--guests`` switch.

    **Example**

    .. code-block:: console

       $ matrixctl users --no-bots
       +----------------+---------------+------------+------------+
       | Name           | Deactivated   | Is Admin   | Is Guest   |
       |----------------+---------------+------------+------------|
       | dunder_mifflin | False         | True       | False      |
       | dwight         | False         | True       | False      |
       | pam            | False         | False      | False      |
       | jim            | False         | False      | False      |
       | creed          | False         | False      | False      |
       | stanley        | False         | False      | False      |
       | kevin          | False         | False      | False      |
       | angela         | False         | False      | False      |
       | phyllis        | False         | False      | False      |
       | tobi           | False         | False      | False      |
       | michael        | False         | True       | False      |
       | andy           | False         | False      | False      |
       +----------------+---------------+------------+------------+

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param cfg:       The ``Config`` class
    :return:          None
    """

    with Api(cfg.api_domain, cfg.api_token) as api:
        len_domain = len(cfg.api_domain) + 1  # 1 for :
        from_user: int = 0
        users: list = []

        while True:
            lst: JsonDict = api.users(from_user, show_guests=arg.guests)

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


def generate_user_tables(
    user_dict: dict, len_domain: int
) -> List[List[Tuple[Any]]]:
    """This function is a recursive function, that generates a main user table
    and a additional table for every threepid from a ``user_dict``.
    It renames and makes the output human readable.

    :param user_dict:   A JSON string which was converted to a Python
                        dictionary.
    :param len_domain:  The length in characters of the domain.
    :return:            The generated lists in this format:
                        [main], threepids_0, ... ,threepids_n]
    """

    table: List[List[Tuple[Any]]] = [[]]

    for k in user_dict:
        if k == "errcode":
            error("There is no user with that username.")
            sys.exit(1)
        key: Optional[str] = None

        if k == "threepids":
            for tk in user_dict[k]:
                ret: Tuple[List[Tuple[Any]]] = generate_user_tables(
                    tk, len_domain
                )
                table.append(ret[0])

            continue  # Don't add threepids to "table"

        if k == "name":
            value = user_dict[k][1:-len_domain]
        elif k == "is_guest":
            value = bool(int(user_dict[k]))
            key = "Guest"
        elif k in ("admin", "deactivated"):
            value = bool(int(user_dict[k]))
        elif k.endswith("_ts"):
            value = str(datetime.datetime.fromtimestamp(user_dict[k]))  # UTC?
        elif k.endswith("_at"):
            value = str(
                datetime.datetime.fromtimestamp(user_dict[k] / 1000.0)
            )  # UTC?

        else:
            value: str = user_dict[k]

        if key is None:
            key = k.replace("_", " ").title()

        table[0].append((key, value))

    return table


def user(arg: Namespace, cfg: Config) -> None:
    """This function lists information about an registered user.
    It uses the admin API to get a python dictionary with the information.
    The ``generate_user_tables`` function makes the information human readable.
    The Python package ``tabulate`` renders the table as shown below, if
    everything works well.


    .. code-block:: console

       $ matrixctl user dwight
       User:
       +----------------------------+--------------------------------------------------------------+
       | Name                       | dwight                                                       |
       | Password Hash              | $2b$12$9DUNderm1ffL1NincPap3RCompaNY1725.slOUghAvEnu5cranT0n |
       | Guest                      | False                                                        |
       | Admin                      | True                                                         |
       | Consent Version            |                                                              |
       | Consent Server Notice Sent |                                                              |
       | Appservice Id              |                                                              |
       | Creation Ts                | 2020-04-14 13:04:21                                          |
       | User Type                  |                                                              |
       | Deactivated                | False                                                        |
       | Displayname                | Dwight Schrute                                               |
       | Avatar Url                 | mxc://dunder-mifflin.com/sCr4nt0nsr4ng13rW45Cr33d            |
       +----------------------------+--------------------------------------------------------------+

       Threepid:
       +--------------+-----------------------------------+
       | Medium       | email                             |
       | Address      | dwight_schrute@dunder-mifflin.com |
       | Validated At | 2020-04-14 15:30:21.123000        |
       | Added At     | 2020-04-14 15:29:19.100000        |
       +--------------+-----------------------------------+

    If the user does not exist, the return looks like:


    .. code-block:: console

       $ matrixctl user mose
       2020-04-14 13:58:13 - ERROR - The request was not successful.
       2020-04-14 13:58:13 - ERROR - There is no user with that username.

    :param arg:       The ``Namespace`` object of argparse's ``arse_args()``
    :param cfg:       The ``Config`` class
    :return:          None
    """

    with Api(cfg.api_domain, cfg.api_token) as api:
        user_str: str = f"@{arg.user}:{cfg.api_domain}"
        user: JsonDict = api.user(user_str)

        len_domain = len(cfg.api_domain) + 1  # 1 for :
        user_tables = generate_user_tables(user, len_domain)

        debug(f"User: {user_tables=}")

        for num, table in enumerate(user_tables):

            if num < 1:
                print("User:")
            else:
                print("\nThreepid:")
            print(tabulate(table, tablefmt="psql",))


# vim: set ft=python :
