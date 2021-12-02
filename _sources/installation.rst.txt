Installation
============

Prerequisites
*************

To be able to use **all** features of MatrixCtl you need to have:

- `Python <https://www.python.org/downloads/>`_ 3.8 or
  higher on your machine.
- deployed the instance of
  `synapse <https://github.com/matrix-org/synapse>`_ with the
  `spantaleev/matrix-docker-ansible-deploy <https://github.com/spantaleev/matrix-docker-ansible-deploy>`_
  ansible playbook.
- the access token of your administrator account.
- SSH access to the matrix server from your machine with a public key.

.. note::  If you don't need all features, you are good to start with
           python 3.8. This is the only mandatory prerequisite of this list.

.. seealso:: We have a guide, how you accomplish the rest of the list in the
             :ref:`Getting Started` guide.

Installation with pip
*********************

To install MatrixCtl run ``pip install matrixctl`` with a ``Python>=3.8``.
If you already have a version of MatrixCtl installed, you can upgrade it with
``pip install --upgrade matrixctl``.

.. Installation on Arch linux
   **************************

   To install MatrixCtl on Arch Linux, you can use the AUR.
   Run ``yay -S python-matrixctl-git``.
