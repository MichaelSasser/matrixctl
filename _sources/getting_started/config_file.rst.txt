Config File
***********

To use this program you need to have this config file in
``/etc/matrixctl/config.yaml`` or in ``~/.config/matrixctl/config.yaml``.

This config file contains four sections:

- ``ansible``
- ``synapse``
- ``api``
- ``ssh``
- ``database``

In ``ansible`` fill in the absolute path to your fully configured
Playbook. Make sure ansible is configured correctly on your system.
To get started, follow the :ref:`Synapse Playbook` guide.
You need this section, if you want to use one of the following commands:

- ``matrixctl adduser --ansible``
- ``matrixctl deploy``
- ``matrixctl start``
- ``matrixctl restart``
- ``matrixctl maintenance``
- ``matrixctl check``

.. note:: If you want to run more than one playbook you can create a file which
          contains ``import_playbook`` lines like:
          ``- import_playbook: /PathTo/matrix-docker-ansible-deploy/setup.yml``
          and configure it as playbook in the matrixctl config file.

``synapse`` is used to update (``git pull``) the synapse playbook
You need this section, if you want to:

- ``matrixctl update``

``api`` is used to communicate with the synapse API directly.
This is faster and has more additional functionality then the
`Synapse <https://github.com/spantaleev/matrix-docker-ansible-deploy>`_
playbook. To get started, follow the :ref:`Access Token` guide.
It is used for:

- ``matrixctl adduser``
- ``matrixctl deluser``
- ``matrixctl users``
- ``matrixctl user``
- ``matrixctl users``
- ``matrixctl upload``
- ``matrixctl rooms``
- ``matrixctl delroom``
- ``matrixctl server-notice``
- ``matrixctl purge-history``
- ``matrixctl version``
- ``matrixctl delete-local-media``
- ``matrixctl get-event-context``
- ``matrixctl is-admin``
- ``matrixctl joinroom``
- ``matrixctl make-room-admin``
- ``matrixctl purge-remote-media``
- ``matrixctl report``
- ``matrixctl reports``
- ``matrixctl set-admin``

``ssh`` you can use additional functionality.
It is used for:

- ``matrixctl adduser-jisi``
- ``matrixctl deluser-jisi``

.. note:: If you are not sure, what to fill in that config file, read the rest
          of the "Getting Started" section of this documentation.

.. warning:: Make sure, that other accounts of your local machine are not able
             to read or edit your config file. I contains sensitive data.

.. include::  config_file_snippet.rst

If you configure ``database``, you can use the following commands:

- ``matrixctl get-event``
- ``matrixctl get-events``

.. note:: You need to create a new PostgreSQL role.
          The must have the permission to login and ``SELECT`` permissions
          for the ``json_events`` and ``events`` table.
