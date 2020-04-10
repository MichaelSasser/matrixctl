![GitHub](https://img.shields.io/github/license/MichaelSasser/matrixctl?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/matrixctl?style=flat-square)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/matrixctl?style=flat-square)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/michaelsasser/matrixctl?style=flat-square)
![GitHub Release Date](https://img.shields.io/github/release-date/michaelsasser/matrixctl?style=flat-square)
![PyPI - Status](https://img.shields.io/pypi/status/matrixctl?style=flat-square)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/michaelsasser/matrixctl?style=flat-square)

# MatrixCtl

MatrixCtl is a python program to control, manage, provision and deploy our
matrix homeserver. I had a bunch of shell scripts doing that. Two weeks
after using them I couldn't remember the order in which I have to use the
arguments or which arguments where needed. It was a pain. So I decided I hack
something together fast.

It is not the most elegant piece of software I wrote, but it should do the
trick. I will continue to port the rest of the scripts and add a few new
features.

Maybe it is also useful for someone else.

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
but breaking changes may be introduced, even in a minor change.

```
# matrixctl
usage: matrixctl [-h] [--version] [-d]
              {adduser,adduser-jitsi,deluser-jitsi,list-users,deluser,deploy,update,maintainance} ...

positional arguments:
  {adduser,adduser-jitsi,deluser-jitsi,list-users,deluser,deploy,update,maintainance}
    adduser             Add a new matrix user
    adduser-jitsi       Add a new jitsi user
    deluser-jitsi       Deletes a jitsi user
    list-users          Lists users
    deluser             Deletes a user
    deploy              Provision and deploy
    update              Updates the ansible repo
    maintainance        Run Maintainance tasks

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d, --debug           Enables debugging mode.
```

## Configuration File

To use this program you need to have this config file in
"/etc/matrixctl/config" or in "~/.config/matrixctl/config".

```toml
[ANSIBLE]
# The absolute path to the fully configured matrix-docker-ansible-deploy
# playbook from https://github.com/spantaleev/matrix-docker-ansible-deploy.

MatrixDockerAnsibleDeployPath="/absolut/path/to/matrix-docker-ansible-deploy"

[SERVER]
# If you have your own playbook, to provision your matrix server, you can
# fill out this section. MatrixCtl will run this before the
# matrix-docker-ansible-deploy playbook.

# If you have a special "ansible.cfg" for your playbook, fill in the absolute
# path to it.

# AnsibleCfg="/absolute/path/to/ansible.cfg"

# Fill in the absolute path to your "site.yml"

# AnsiblePlaybook="/absolute/path/to/site.yml"

# If you use tags to provision or configure your matrix host, you can add them
# here. Use a comma separated string without spaces.

# AnsibleTags="MyTag,MyOtherTag"

[API]
# If your matrix server is deployed, you may want to fill out the API section.
# It enables matrixctl to run more and faster commands. You can deploy and
# provision your Server without this section. You also can cerate a user with
# "matrixctl adduser --ansible YourUsername" and add your privileges after
# that.

# Your domain should be something like "michaelsasser.org" without the
# "matrix." in the front. MatrixCtl will add that, if needed. An IP-Address
# is not enough.

# Domain="domain.tld"

# To use the API you need to have an administrator account. Enter your Token
# here. If you use the riot client you will find it your user settings (click
# on your username on the upper left corner on your browser) in the
# "Help & About" tab. If you scroll down click next to "Access-Token:" on
# "<click to reveal>". It will be marked for you. Copy it in here.

# Token="MyMatrixToken"
```

## Semantic Versioning

**After release "1.0.0"** this repository will use
[SemVer](https://semver.org/) for its release
cycle.

**Before release "1.0.0"** it uses "0.MAJOR.MINOR_or_PATCH".
This means, if breaking changes are introduced, it results in a major version
change (e.g. "0.1.0" -> "0.2.0"). Minor changes, like new features or patches
are bumping the last digit (e.g. "0.1.1" -> "0.1.2").

## License
Copyright &copy; 2020 Michael Sasser <Info@MichaelSasser.org>. Released under
the GPLv3 license.
