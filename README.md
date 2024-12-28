![GitHub](https://img.shields.io/github/license/MichaelSasser/matrixctl?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/matrixctl?style=flat-square)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/michaelsasser/matrixctl?style=flat-square)
![GitHub Release Date](https://img.shields.io/github/release-date/michaelsasser/matrixctl?style=flat-square)
![Matrix](https://img.shields.io/matrix/matrixctl:matrix.org?server_fqdn=matrix.org&style=flat-square)

# MatrixCtl

MatrixCtl is a simple, but feature-rich tool to remotely control, manage,
provision and deploy your Matrix homeservers and users from your virtual
terminal.

```console
$ matrixctl
usage: matrixctl [-h] [--version] [-d] [-s SERVER] [-c CONFIG] Command ...

MatrixCtl is a simple, but feature-rich tool to remotely control, manage, provision and deploy Matrix homeservers.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d, --debug           Enables debugging mode.
  -s SERVER, --server SERVER
                        Select the server. (default: "default")
  -c CONFIG, --config CONFIG
                        A path to an alternative config file.

Commands:
  The following are commands, you can use to accomplish various tasks.

  Command
    adduser             Add users to the homeserver
    check               Checks the deployment with Ansible
    delete-local-media  Delete cached (local) media that was last accessed before a specific point in time
    delroom             Shutdown a room
    deluser             Deactivate users
    deploy              Provision and deploy the Ansible playbook
    download            Download a media file.
    get-event           Get an event from the database
    get-event-context   Get the context of an event
    get-events          Get events from the database
    is-admin            Check, if a user is a homeserver administrator
    joinroom            Join a user to a room
    largest-rooms       List an approximation of the 10 largest rooms in the database
    maintenance         Run maintenance tasks
    make-room-admin     Grant a user the highest power level available to a local user in this room
    purge-history       Purge historic events from the database
    purge-remote-media  Purge cached, remote media
    report              Get a report event by report identifier
    reports             Lists reported events
    rooms               List rooms
    server-notice       Send a server notice to a user
    set-admin           Change whether a user is a homeserver admin or not
    start               Starts all OCI containers
    restart             Restarts all OCI containers (alias for start)
    stop                Stop and disable all OCI containers
    update              Updates the ansible playbook repository
    upload              Upload a media file.
    user                Get information about a specific user
    users               Lists all users of the homeserver
    version             Get the version information of the Synapse instance

Thank you for using MatrixCtl!
Check out the docs: https://matrixctl.rtfd.io
Report bugs to: https://github.com/MichaelSasser/matrixctl/issues/new/choose
```

## Installation

MatrixCtl is written in Python. The installation is straight forward. Just run
`pip install matrixctl`. It will be installed from the
[Python Package Index (PyPi)](https://pypi.org/project/matrixctl/).

Upgrade MatrixCtl with `pip install --upgrade matrixctl`.

You will find more information in the
[documentation](https://matrixctl.readthedocs.io/en/latest/installation.html).

## Documentation

The [documentation](https://matrixctl.readthedocs.io/en/latest/index.html) is
waiting for you, to check out.

## Configuration File

To use this tool you need to have a configuration file in
"~/.config/matrixctl/config.yaml" or in "/etc/matrixctl/config.yaml".

```yaml
# Define your homeservers in "servers" here.
servers:
  # Your default server. You can specify muliple servers here with arbitrary
  # Names
  default:
    ansible:
      # The absolute path to your playbook
      playbook: /path/to/ansible/playbook

    synapse:
      # The absolute path to the synapse playbook.
      # This is only used for updating the playbook.
      playbook: /path/to/synapse/playbook

    # If your matrix server is deployed, you may want to fill out the API section.
    # It enables matrixctl to run more and faster commands. You can deploy and
    # provision your Server without this section. You also can create a user with
    # "matrixctl adduser --ansible YourUsername" and add your privileges after
    # that.
    api:
      # Your domain should be something like "michaelsasser.org" without the
      # "matrix." in the front. MatrixCtl will add that, if needed. An IP-Address
      # is not enough.
      domain: example.com

      # The username your admin user
      username: johndoe

      # To use the API you need to have an administrator account. Enter your Token
      # here. If you use the element client you will find it your user settings
      # (click on your username on the upper left corner on your browser) in the
      # "Help & About" tab. If you scroll down click next to "Access-Token:" on
      # "<click to reveal>". It will be marked for you. Copy it in here.
      token: "MyMatrixToken"

      # In some cases, MatrixCtl does need to make many requests. To speed those
      # requests a notch, you can set a concurrent_limit which is greater than
      # one. This sets a limit to how many asynchronous workers can be spawned
      # by MatrixCtl. If you set the number to high, MatrixCtl needs more time
      # to spawn the workers, then a synchronous request would take.
      concurrent_limit: 10

    # Here you can add your SSH configuration.
    ssh:
      address: matrix.example.com

      # The default port is 22
      port: 22

      # The default username is your current login name.
      user: john

    # Define your maintenance tasks
    maintenance:
      tasks:
        - compress-state # Compress synapses state table
        - vacuum # VACUUM the synapse database (garbage-collection)

    # Add connection parameters to the Database
    # Synapse does only read (SELECT) information from the database.
    # The user needs to be able to login to the synapse database
    # and SELECT from the events and event_json tables.
    database:
      synapse_database: synapse # this is the playbooks default table name
      synapse_user: matrixctl # the username (role) for the database
      synapse_password: "RolePassword"
      tunnel: true # true if an ssh tunnel should be used to connect

      # The port that was used in the playbook  (e.g.
      # matrix_postgres_container_postgres_bind_port: 5432)
      # or for your external database. For security reasons the port
      # should be blocked by your firewall. Iy you enable the tunnel
      # by setting tunnel: true, MatrixCtl activates a SSH tunnel.
      port: 5432 # the remote port

  # Another server.
  foo:
    # ...
```

Predefined Jinja2 placeholders (all placeholders can be overwritten):

- `"{{ home }}"` -- The current users home path e.g. `/home/michael`,
- `"{{ user }}"` -- The current users username e.g. `michael`,
- `"{{ default_ssh_port }}"` -- The default ssh port `22`,
- `"{{ default_api_concurrent_limit }}"` -- The default concurrent limit `4`.

Check out the
[documentation](https://matrixctl.readthedocs.io/en/latest/getting_started/config_file.html)
for more information.

## Discussions & Chat

If you have any thoughts or questions, you can ask them in the
[discusions](https://github.com/MichaelSasser/matrixctl/discussions) or in the
projects matrix room `#matrixctl:matrix.org`.

## Semantic Versioning and Branching Model

This Python package uses [SemVer](https://semver.org/) for its release cycle
and follows the
[GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow).

## Contributing

Please check our
[Contributer Documentation](https://matrixctl.readthedocs.io/en/latest/contributer_documentation/index.html#contributer-documentation).

## License

Copyright &copy; 2020-2001 Michael Sasser <Info@MichaelSasser.org>. Released
under the GPLv3 license.
