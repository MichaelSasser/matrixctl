![GitHub](https://img.shields.io/github/license/MichaelSasser/matrixctl?style=flat-square)

# MatrixCtl

MatrixCtl is a python program to control, manage, provision and deploy our
matrix homeserver. I had a bunch of shell scripts doing that. Two weeks
after using them I couldn't remember the order in which I have to use the
arguments. It was a pain. So I decided I hack something together fast.

It is not the most elegant piece of software I wrote, but it should do the
trick for now. I will continue to port the rest of the scripts. Maybe
it is also useful for someone else.

```
# matrixctl
usage: matrixctl [-h] [--version] [-d] {adduser,deluser,deploy,update,maintainance} ...

positional arguments:
  {adduser,deluser,deploy,update,maintainance}
    adduser             Add a user
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
# playbook.

MatrixDockerAnsibleDeployPath="/absolut/path/to/matrix-docker-ansible-deploy"

[SERVER]
# If you have your own playbook, to provision your matrix server, you can
# fill out the server section. matrixctl will run it before the
# matrix-docker-ansible-deploy playbook.

# AnsibleCfg="/absolut/path/to/ansible.cfg"
# AnsiblePlaybook="/absolut/path/to/site.yml"
# AnsibleTags="MyTag,MyOtherTag"

[API]
# If your matrix server is deployed, you may want to fill out the API section.
# It enables matrixctl to run more and faster commands. You can deploy and
# provision your Server without this section. You also can cerate a user with
# "matrixctl adduser --ansible YourUsername" and add your privileges after
# that.

# Domain="domain.tld"
# Token="MyMatrixToken"
```

## License
Copyright &copy; 2020 Michael Sasser <Info@MichaelSasser.org>.
Released under the GPLv3 license.
