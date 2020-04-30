Config File
***********

To use this program you need to have this config file in
``/etc/matrixctl/config`` or in ``~/.config/matrixctl/config``.

This config file contains four sections:

- ``[SYNAPSE]``
- ``[ANSIBLE]``
- ``[API]``
- ``[SSH]``

In the ``[SYNAPSE]`` section fill in the absolute path to your fully configured
`Synapse <https://github.com/spantaleev/matrix-docker-ansible-deploy>`_
playbook. To get started, follow the :ref:`Synapse Playbook` guide.
You need this section, if you want to:

- ``matrixctl adduser --ansible``
- ``matrixctl update``
- ``matrixctl deploy``
- ``matrixctl start``
- ``matrixctl restart``
- ``matrixctl maintenance``
- ``matrixctl check``

With the ``[ANSIBLE]`` section you can add your own playbook, if you like.
It will run on ``update`` before  the
`Synapse <https://github.com/spantaleev/matrix-docker-ansible-deploy>`_
playbook.
It is used for:

- ``matrixctl update`` (optional)

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
