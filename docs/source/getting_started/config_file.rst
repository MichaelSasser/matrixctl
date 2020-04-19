Config File
***********

To use this program you need to have this config file in
``/etc/matrixctl/config`` or in ``~/.config/matrixctl/config``.

This config file contains three sections:

- ``[ANSIBLE]``
- ``[SERVER]``
- ``[API]``

In the ``[ANSIBLE]`` section fill in the absolute path to your fully configured
`matrix-docker-ansible-deploy <https://github.com/spantaleev/matrix-docker-ansible-deploy>`_
playbook. To get startet, follow the :ref:`Synapse Playbook` guide.
You need this section, if you want to:

- ``matrixctl adduser --ansible``
- ``matrixctl update``
- ``matrixctl deploy``
- ``matrixctl start``
- ``matrixctl restart``
- ``matrixctl maintainance``
- ``matrixctl check``

With the ``[SERVER]`` section you can add your own playbook, if you like.
It will run on ``update`` before  the
`matrix-docker-ansible-deploy <https://github.com/spantaleev/matrix-docker-ansible-deploy>`_
playbook.
It is used for:

- ``matrixctl update`` (optional)

The ``[API]`` section is used to communicate with the synapse api directly.
This is faster and has more additional functionality then the
`matrix-docker-ansible-deploy <https://github.com/spantaleev/matrix-docker-ansible-deploy>`_
playbook. To get startet, follow the :ref:`Access Token` guide.
It is used for:

- ``matrixctl adduser``
- ``matrixctl deluser``
- ``matrixctl users``
- ``matrixctl user``

.. note:: If you are not sure, what to fill in that config file, read the rest
          of the "Getting Started" section of this documentation.

.. warning:: Make sure, that other accounts of your local machine are not able
             to read or edit your config file. I contains sensitive data.

.. include::  config_file_snippet.rst
