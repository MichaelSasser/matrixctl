..
   matrixctl
   Copyright (c) 2021  Michael Sasser <Michael@MichaelSasser.org>

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.

=========================
Contributor Documentation
=========================

First off, thank you for considering contributing to MatrixCtl. Please make sure
to read our Code of Conduct before you start Contributing to MatrixCtl.

.. include::  coc.rst

I found a bug / I want to give feedback
=======================================

If you found a bug or you want to give feedback, please create an `issue
<https://github.com/MichaelSasser/matrixctl/issues/new/choose>`_ using
one of the templates.

I have a question
=================

Please check the
`discussions <https://github.com/MichaelSasser/matrixctl/discussions>`_ first.
When you don't find the right thread, feel free to create a new one.

Add a feature
=============

.. note:: Before you start make sure you hand in an `issue
          <https://github.com/MichaelSasser/matrixctl/issues/new/choose>`_.
          Describe, what you like to change/add, so others are informed, what
          you are about to change and why you want to change anything.

1. Make sure you have at least ``Python 3.10``,
   `uv <https://docs.astral.sh/uv/>`_, and the plugin
   `tox-uv <https://github.com/tox-dev/tox-uv/>`_ installed.
2. Create a fork of MatrixCtl.
3. Clone the fork (``origin``) to your local machine.
4. Add the original repository as a remote named ``upstream``.
5. Create a new branch from the
   `main branch <https://github.com/MichaelSasser/matrixctl>`_.
   Make sure you use the
   `GitHub Flow <https://docs.github.com/en/get-started/using-github/github-flow>`_.
   For example:
   Let's say your issue was issue ``#42`` and you want to create a feature.
   Your branch name would be ``feature/#42`` or ``feature/#42-my-cool-feature``.
#. Install the required tools with ``rye sync --all-extras --dev``
#. Implement your feature or fix the bug you described in your issue.
#. Create a ``Pull Request`` as soon as possible as ``draft``, so other
   contributors are able to help you and follow your progress.
#. Make sure to add/alter the documentation.
#. Add/alter tests, to test your code.
#. Run ``make tox``. If everything is green with no errors, you are good to go.
#. Describe your changes using
   `Conventional Commits <https://www.conventionalcommits.org/en/>`_.
#. Publish your branch to your fork (``origin``).
#. Create a pull request from the Branch, which contains your changes to
   MatrixCtl's ``main`` branch.
#. Once the pull request is reviewed and merged you can pull the changes from
   ``upstream`` (the original repository) to your local repository and start
   over again from ``5.``. Don't forget to create an issue first.

.. note:: Do not add any additional requirement without an approval first. Make
          sure to use the provided ``Handlers``, ``Helpers``, ``Errors``
          (``exceptions``) and ``Type Hints``.

.. note:: If you have any questions feel free to ask in the issues, pull
          requests and discussions.

.. note:: You often can use one of the :ref:`Commands` as template for a new
          addon.

.. toctree::
   :maxdepth: 1
   :caption: Technical Documentation:

   handlers
   helpers
   type_hints_structures_and_errors
   commands
   application
   tests

..
   vim: set ft=rst :
