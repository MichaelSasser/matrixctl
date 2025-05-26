![GitHub](https://img.shields.io/github/license/MichaelSasser/matrixctl?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/matrixctl?style=flat-square)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/michaelsasser/matrixctl?style=flat-square)
![GitHub Release Date](https://img.shields.io/github/release-date/michaelsasser/matrixctl?style=flat-square)
![Matrix](https://img.shields.io/matrix/matrixctl:matrix.org?server_fqdn=matrix.org&style=flat-square)

# MatrixCtl

MatrixCtl is a simple, but feature-rich tool to remotely control, manage,
provision and deploy your Matrix homeservers right from your virtual terminal.

```console
usage: matrixctl [-h] [-d] [-S SERVER] [-c CONFIG] [--version] Category ...

MatrixCtl is a simple, but feature-rich tool to remotely control, manage, provision and deploy Matrix homeservers.

options:
  -h, --help           show this help message and exit
  -d, --debug          Enables debugging mode.
  -S, --server SERVER  Select the server. (default: "default")
  -c, --config CONFIG  A path to an alternative config file.
  --version            show program's version number and exit

Categoties:
  Please select a category to see the available commands.

  Category
    room               Manage rooms.
    user               Manage users.
    media              Manage media files on the server.
    server             Manage the homeserver instance.
    mod                Moderation commands for rooms and users.
    self               Manage MatrixCtl.

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
  # Your default server. You can specify multiple servers here with arbitrary
  # Names
  default:
    alias:
      # Remembering internal room identifiers is not your strong suit?
      # Mine neither. Therefore you can define some aliases for your rooms.
      # They will be automatically translated to the internal room IDs.
      room:
        - {name: test, room_id: "!BuuJZEbstPPYUZgbt:michaelsasser.org"}
        - {name: mjolnir, room_id: "!mJoLnIrRoOm:matrix.org"}
        - {name: foo, room_id: "!fO0BArBAzFJTbhaTvU:michaelsasser.org"}

    ansible:
      # The absolute path to your playbook
      playbook: /path/to/ansible/playbook

    synapse:
      # The absolute path to the synapse playbook.
      # This is only used for updating the playbook.
      playbook: /path/to/synapse/playbook

    # If your matrix server is deployed, you may want to fill out the API section.
    # It enables MatrixCtl to run more and faster commands. You can deploy and
    # provision your Server without this section. You also can create a user with
    # "matrixctl user adduser --ansible YourUsername" and add your privileges after
    # that.
    api:
      # Your domain should be something like "michaelsasser.org" without the
      # "matrix." in the front. MatrixCtl will add that, if needed. An IP-Address
      # is not enough.
      domain: example.com

      # How you want to authenticate. The default is "token". You can also use
      auth_type: oidc # possible values: oidc, token

      # Only required if you use the token authentication method (auth_type)
      auth_token:
        # The localpart of your admin user
        username: johndoe # johndoe from @johndoe:example.com

        # To use the API you need to have an administrator account. Enter your Token
        # here. If you use the element client you will find it your user settings
        # (click on your username on the upper left corner on your browser) in the
        # "Help & About" tab. If you scroll down click next to "Access-Token:" on
        # "<click to reveal>". It will be marked for you. Copy it in here.
        token: "MyMatrixToken"

      # Only required if you use the OIDC authentication method (auth_type)
      # To get more information about the OIDC authentication method, check out
      # docs.
      auth_oidc:
        discovery_endpoint: https://mas.yourdomain.tld/.well-known/openid-configuration
        client_id: 01JVZSJNTM8EPFCA9R55V2PFW9
        client_secret: 7eQgWf5XIwIVkrVmzc5nxw731u4Riu16YK1oHOfTDR2xU4iD7C7ijiSD8wclfTDn

        # Optional, when discovery_endpoint is not set or to overwrite the
        # the discovered values.

        # token_endpoint:
        # auth_endpoint:
        # userinfo_endpoint:
        # jwks_uri:

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
- `"{{ well_knowen_path }}"` -- The OIDC well-known path
  `.well-known/openid-configuration`.

Check out the
[documentation](https://matrixctl.readthedocs.io/en/latest/getting_started/config_file.html)
for more information.

## Discussions & Chat

If you have any thoughts or questions, you can ask them in the
[discusions](https://github.com/MichaelSasser/matrixctl/discussions) or in the
projects matrix room `#matrixctl:matrix.org`.

## Versioning and Branching Model

This Python package follows the
[PyPA](https://packaging.python.org/en/latest/specifications/) specification
for its release cycle and follows the
[GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow).

## Contributing

Please check our
[Contributer Documentation](https://matrixctl.readthedocs.io/en/latest/contributer_documentation/index.html#contributer-documentation).

## License

Copyright &copy; 2020-2024 Michael Sasser <Info@MichaelSasser.org>. Released
under the GPLv3 license.
