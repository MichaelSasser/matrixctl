![GitHub](https://img.shields.io/github/license/MichaelSasser/matrixctl?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/matrixctl?style=flat-square)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/matrixctl?style=flat-square)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/michaelsasser/matrixctl?style=flat-square)
![GitHub Release Date](https://img.shields.io/github/release-date/michaelsasser/matrixctl?style=flat-square)
![PyPI - Status](https://img.shields.io/pypi/status/matrixctl?style=flat-square)
![Matrix](https://img.shields.io/matrix/matrixctl:michaelsasser.org?server_fqdn=matrix.org&style=flat-square)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/michaelsasser/matrixctl?style=flat-square)

# MatrixCtl

MatrixCtl is a python program to control, manage, provision and deploy our
matrix homeserver. Instead of remembering tons of commands or having a bunch
of shell scripts MatrixCtl does many things for you.

## Command line tool

MatrixCtl as a pure commandline tool. You can use it as package, if you like,
but breaking changes may be introduced, even in a minor version shift.

```
# matrixctl
usage: matrixctl [-h] [--version] [-d]
                 {adduser,deluser,adduser-jitsi,deluser-jitsi,user,users,rooms,delroom,update,upload,deploy,server-notice,start,restart,maintenance,check,version}
              ...

positional arguments:
  {adduser,deluser,adduser-jitsi,deluser-jitsi,user,users,rooms,delroom,update,upload,deploy,server-notice,start,restart,maintenance,check,version}
    adduser             Add a new matrix user
    deluser             Deletes a user
    adduser-jitsi       Add a new jitsi user
    deluser-jitsi       Deletes a jitsi user
    user                Get information about a specific user
    users               Lists users
    rooms               List rooms
    delroom             Deletes an empty room from the database
    update              Updates the ansible repo
    upload              Upload a file.
    deploy              Provision and deploy
    server-notice       Send a server notice
    start               Starts all OCI containers
    restart             Restarts all OCI containers (alias for start)
    maintenance         Run maintenance tasks
    check               Checks the OCI containers
    version             Get the version of the Synapse instance

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d, --debug           Enables debugging mode.
```

## Installation

MatrixCtl is written in Python. The installation is straight forward. Just run ``pip install matrixctl``. MatrixCtl will be installd from the [Python Package Index (PyPi)](https://pypi.org/project/matrixctl/).

You will find more information in the documentation.

## Documentation

There is a [documentation](https://michaelsasser.github.io/matrixctl/index.html) waiting for you, showing you how everything works and howto setup matrixctl

## Configuration File

To use this program you need to have this config file in
"/etc/matrixctl/config" or in "~/.config/matrixctl/config".

Check out the documentation for more information.

```toml
[ANSIBLE]
# The absolute path to your playbook
#
# Playbook="/absolut/path/to/the/playbook"

[SYNAPSE]
# The absolute path to the synapse playbook.
# This is only used for updating the playbook.
#
# Playbook = "/absolut/path/to/the/playbook"

[API]
# If your matrix server is deployed, you may want to fill out the API section.
# It enables matrixctl to run more and faster commands. You can deploy and
# provision your Server without this section. You also can cerate a user with
# "matrixctl adduser --ansible YourUsername" and add your privileges after
# that.

# Your domain should be something like "michaelsasser.org" without the
# "matrix." in the front. MatrixCtl will add that, if needed. An IP-Address
# is not enough.
#
# Domain = "domain.tld"

# To use the API you need to have an administrator account. Enter your Token
# here. If you use the element client you will find it your user settings (click
# on your username on the upper left corner on your browser) in the
# "Help & About" tab. If you scroll down click next to "Access-Token:" on
# "<click to reveal>". It will be marked for you. Copy it in here.
#
# Token= " MySuperLongMatrixToken"

[SSH]
# Here you can add your SSH configuration.
#
# Address = "matrix.domain.tld"

# The default port is 22
#
# Port = 22

# The default username is your current login name.
#
# User = "MyUserSystemAccountName"
```

## Chat

If you have any thoughts or questions, you can join the project channel ``#matrixctl:michaelsasser.org``.

## Semantic Versioning

This repository uses [SemVer](https://semver.org/) for its release
cycle.

## Branching Model

This repository uses the
[git-flow](https://danielkummer.github.io/git-flow-cheatsheet/index.html)
branching model by [Vincent Driessen](https://nvie.com/about/).
It has two branches with infinite lifetime:

* [master](https://github.com/MichaelSasser/matrixctl/tree/master)
* [develop](https://github.com/MichaelSasser/matrixctl/tree/develop)

The master branch gets updated on every release. The develop branch is the
merging branch.

## License
Copyright &copy; 2020-2001 Michael Sasser <Info@MichaelSasser.org>.
Released under the GPLv3 license.
