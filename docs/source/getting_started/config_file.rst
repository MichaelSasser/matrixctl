Config File
***********

To use this program you need to have this config file in
``/etc/matrixctl/config`` or in ``~/.config/matrixctl/config``.

This config file contains four sections:

- ``[ANSIBLE]``
- ``[SYNAPSE]``
- ``[API]``
- ``[SSH]``

In the ``[ANSIBLE]`` section fill in the absolute path to your fully configured
Playbook. Make sure ansible is configured correctly on your system.
To get started, follow the :ref:`Synapse Playbook` guide.
You need this section, if you want to:

- ``matrixctl adduser --ansible``
- ``matrixctl deploy``
- ``matrixctl start``
- ``matrixctl restart``
- ``matrixctl maintenance``
- ``matrixctl check``

.. note:: If you want to run (multible) playbooks you can create a file which
          contains ``import_playbook`` lines like:
          ``- import_playbook: /PathTo/matrix-docker-ansible-deploy/setup.yml``
          and configure it as playbook in the matrixctl config file.

The ``[SYNAPSE]`` section is used for update (``git pull``) the synapse
playbook
You need this section, if you want to:

- ``matrixctl update``

The ``[API]`` section is used to communicate with the synapse API directly.
This is faster and has more additional functionality then the
`Synapse <https://github.com/spantaleev/matrix-docker-ansible-deploy>`_
playbook. To get started, follow the :ref:`Access Token` guide.
It is used for:

- ``matrixctl adduser``
- ``matrixctl deluser``
- ``matrixctl users``
- ``matrixctl user``

With the ``[SSH]`` section you can use additional functionality, if you like.
It is used for:

- ``matrixctl adduser-jisi``
- ``matrixctl deluser-jisi``

.. note:: If you are not sure, what to fill in that config file, read the rest
          of the "Getting Started" section of this documentation.

.. warning:: Make sure, that other accounts of your local machine are not able
             to read or edit your config file. I contains sensitive data.

.. include::  config_file_snippet.rst
