![GitHub](https://img.shields.io/github/license/MichaelSasser/matrixctl?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/matrixctl?style=flat-square)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/matrixctl?style=flat-square)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/michaelsasser/matrixctl?style=flat-square)
![GitHub Release Date](https://img.shields.io/github/release-date/michaelsasser/matrixctl?style=flat-square)
![PyPI - Status](https://img.shields.io/pypi/status/matrixctl?style=flat-square)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/michaelsasser/matrixctl?style=flat-square)

# MatrixCtl

MatrixCtl is a python program to control, manage, provision and deploy our
matrix homeserver. Instead of remembering tons of commands or having a bunch
of shell scripts MatrixCtl does many things for you.

## Branching Model

This repository uses the
[git-flow](https://danielkummer.github.io/git-flow-cheatsheet/index.html)
branching model by [Vincent Driessen](https://nvie.com/about/).
It has two branches with infinite lifetime:

* [master](https://github.com/MichaelSasser/matrixctl/tree/master)
* [develop](https://github.com/MichaelSasser/matrixctl/tree/develop)

The master branch gets updated on every release. The develop branch is the
merging branch.

## Command line tool

MatrixCtl as a pure commandline tool. You can use it as package, if you like,
but breaking changes may be introduced, even in a minor version shift.

```
# matrixctl
usage: matrixctl [-h] [--version] [-d]
              {adduser,deluser,adduser-jitsi,deluser-jitsi,user,users,rooms,delroom,update,deploy,start,restart,maintainance,check,version}
              ...

positional arguments:
  {adduser,deluser,adduser-jitsi,deluser-jitsi,user,users,rooms,delroom,update,deploy,start,restart,maintainance,check,version}
    adduser             Add a new matrix user
    deluser             Deletes a user
    adduser-jitsi       Add a new jitsi user
    deluser-jitsi       Deletes a jitsi user
    user                Get information about a specific user
    users               Lists users
    rooms               List rooms
    delroom             Deletes an empty room from the database
    update              Updates the ansible repo
    deploy              Provision and deploy
    start               Starts all OCI containers
    restart             Restarts all OCI containers (alias for start)
    maintainance        Run maintainance tasks
    check               Checks the OCI containers
    version             Get the version of the Synapse instance

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d, --debug           Enables debugging mode.
```

## Configuration File

To use this program you need to have this config file in
"/etc/matrixctl/config" or in "~/.config/matrixctl/config".

```toml
[SYNAPSE]
# The absolute path to the fully configured matrix-docker-ansible-deploy
# playbook from https://github.com/spantaleev/matrix-docker-ansible-deploy.
#
# Path="/absolut/path/to/matrix-docker-ansible-deploy"

[ANSIBLE]
# If you have your own playbook, to provision your matrix server, you can
# fill out this section. MatrixCtl will run this before the synapse playbook.

# The absolute path to your playbook
#
# Path = "/absolute/path/to/your/playbook"

# If you have a special "ansible.cfg" for your playbook, fill in the absolute
# path to it.
#
# Cfg="/absolute/path/to/ansible.cfg"

# Fill in the absolute path to your Playbook (e.g. "site.yml")
#
# Playbook ="setup.yml"

# If you use tags to provision or configure your matrix host, you can add them
# here.
#
# Tags = ["MyTag", "MyOtherTag"]

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
# Domain="domain.tld"

# To use the API you need to have an administrator account. Enter your Token
# here. If you use the riot client you will find it your user settings (click
# on your username on the upper left corner on your browser) in the
# "Help & About" tab. If you scroll down click next to "Access-Token:" on
# "<click to reveal>". It will be marked for you. Copy it in here.
#
# Token="MySuperLongMatrixToken"

[SSH]
# Here you can add your SSH configuration.
#
# Address = "matrix.domain.tld"

# The default port is 22
#
# Port = 22

# The default username is your current login name.
#
# User = "myusername"
```

## Semantic Versioning

This repository will uses [SemVer](https://semver.org/) for its release
cycle.

## License
Copyright &copy; 2020 Michael Sasser <Info@MichaelSasser.org>. Released under
the GPLv3 license.
