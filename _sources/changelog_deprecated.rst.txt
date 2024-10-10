This is the changelog of MatrixCtl. You can find the issue tracker on
`GitHub <https://github.com/MichaelSasser/matrixctl/issues>`_.

.. towncrier release notes start

0.12.0 (2024-06-05)
==========================

(No significant changes)

0.12.0-beta.2 (2023-03-24)
==========================

Bugfixes
--------

- Fix ``M_UNKNOWN`` bug when using ``purge-history``. (`#165
  <https://github.com/MichaelSasser/matrixctl/issues/165>`_)
- Ensure MatrixCtl does not log the database password for synapse in debug mode
  (`#460 <https://github.com/MichaelSasser/matrixctl/issues/460>`_)


Removals & Deprecations
-----------------------

- Add a deprecation warning to the adduser-jitsi and deluser-jitsi commands.
  They are planned for removal in MatrixCtl v0.13.0. (`#453
  <https://github.com/MichaelSasser/matrixctl/issues/453>`_)


Miscellaneous
-------------

- Add tests to the sanitizers (`#315
  <https://github.com/MichaelSasser/matrixctl/issues/315>`_)
- Update pre-commit plugin flake8 to new repo url (`#448
  <https://github.com/MichaelSasser/matrixctl/issues/448>`_)
- Fix rtd: Invalid configuration option: python.version (`#450
  <https://github.com/MichaelSasser/matrixctl/issues/450>`_)


0.12.0-beta.1 (2021-12-02)
==========================

Behavior & Breaking Changes
---------------------------

- This release changes how MatrixCtl connects to the database. Therefore
  the configuration file must be changed. Please check the
  `documentation <https://matrixctl.readthedocs.io/en/stable/getting_started/config_file.html>`_
  for more information. (`#313
  <https://github.com/MichaelSasser/matrixctl/issues/313>`_)


Features & Improvements
-----------------------

- ``get-event`` and ``get-events`` are not using psycopg instead of a docker
  command (`#313 <https://github.com/MichaelSasser/matrixctl/issues/313>`_)


Bugfixes
--------

- Empty data for the table handler does no longer raise an error. (`#309
  <https://github.com/MichaelSasser/matrixctl/issues/309>`_)
- The message ``Deleted Rooms: 0`` in ``purge-remote-media`` has been corrected
  to ``Deleted Media Files: 0`` (`#311
  <https://github.com/MichaelSasser/matrixctl/issues/311>`_)


0.11.5 (2021-12-01)
===================

No significant changes.


0.11.4 (2021-12-01)
===================

Features & Improvements
-----------------------

- Update to *Delete Room API v2*. (`#305
  <https://github.com/MichaelSasser/matrixctl/issues/305>`_)


Bugfixes
--------

- Fix a bug introduced in ``be411cf0c1a9413bf25ca1b72004150c032555c2``, after
  the last release because the ``httpx`` typehints are incorrect. (`#307
  <https://github.com/MichaelSasser/matrixctl/issues/307>`_)


Miscellaneous
-------------

- Fix incorrect typehints in the API handler (`#287
  <https://github.com/MichaelSasser/matrixctl/issues/287>`_)


0.11.3 (2021-11-16)
===================

Features & Improvements
-----------------------

- Add ``is-admin`` addon to determine if a user is a server admin. (`#252
  <https://github.com/MichaelSasser/matrixctl/issues/252>`_)
- Add ``set-admin`` addon to promote/demote users to/from homeserver admin
  (`#254 <https://github.com/MichaelSasser/matrixctl/issues/254>`_)
- Add make-room-admin addon (`#265
  <https://github.com/MichaelSasser/matrixctl/issues/265>`_)
- Add ``get-event-context`` addon. (`#267
  <https://github.com/MichaelSasser/matrixctl/issues/267>`_)
- Add ``-f|--force`` switch to ``purge-history`` to answer all questions with
  ``yes``. (`#271 <https://github.com/MichaelSasser/matrixctl/issues/271>`_)
- Add ``-e|--empty`` switch argument to ``rooms``, to only show empty rooms.
  (`#273 <https://github.com/MichaelSasser/matrixctl/issues/273>`_)
- Add ``purge-remote-media`` addon. (`#275
  <https://github.com/MichaelSasser/matrixctl/issues/275>`_)
- ``delroom`` now uses the "Delete Room API" instead of the old "Purge Room
  API", which is deprecated. (`#277
  <https://github.com/MichaelSasser/matrixctl/issues/277>`_)
- Add ``delete-local-media`` addon. (`#278
  <https://github.com/MichaelSasser/matrixctl/issues/278>`_)
- Debloat ``matrixctl --help`` (`#281
  <https://github.com/MichaelSasser/matrixctl/issues/281>`_)


Miscellaneous
-------------

- Remove dependency ``single_source`` (`#245
  <https://github.com/MichaelSasser/matrixctl/issues/245>`_)
- Generate the release body with a script while running the release action.
  (`#284 <https://github.com/MichaelSasser/matrixctl/issues/284>`_)


0.11.2 (2021-09-26)
===================

Features & Improvements
-----------------------

- Add the ``joinroom`` (join a user to a room) addon to MatrixCtl. (`#89
  <https://github.com/MichaelSasser/matrixctl/issues/89>`_)


Miscellaneous
-------------

- The API handler was refactored, which results roughly in a 10% speed increase
  for asynchronous requests. (`#235
  <https://github.com/MichaelSasser/matrixctl/issues/235>`_)


0.11.1 (2021-09-25)
===================

Features & Improvements
-----------------------

- ``paramiko`` now creates a ``known_hosts`` entry, if it does not exist.
  (`#231 <https://github.com/MichaelSasser/matrixctl/issues/231>`_)


Bugfixes
--------

- Fix: ``adduser``, ``deluser``, ``delroom``, ``server-notice``,
  ``purge-history``. (`#233
  <https://github.com/MichaelSasser/matrixctl/issues/233>`_)


0.11.0 (2021-09-21)
===================

Behavior & Breaking Changes
---------------------------

- The config file now is using the ``YAML`` format instead of the ``TOML``
  format. (`#174 <https://github.com/MichaelSasser/matrixctl/issues/174>`_)
- Drop support for python 3.8. (`#181
  <https://github.com/MichaelSasser/matrixctl/issues/181>`_)
- The password generation of MatrixCtl has been removed (`#193
  <https://github.com/MichaelSasser/matrixctl/issues/193>`_)
- All servers in the config (``config.yaml``) file now need too be grouped
  below
  ``servers:``. (`#213
  <https://github.com/MichaelSasser/matrixctl/issues/213>`_)
- Remove ``--number`` and ``-n`` in the ``rooms`` addon and replace it with
  ``[limit]``. (`#217
  <https://github.com/MichaelSasser/matrixctl/issues/217>`_)


Features & Improvements
-----------------------

- Add ``rust-synapse-compress-state`` to the maintenance command. (`#163
  <https://github.com/MichaelSasser/matrixctl/issues/163>`_)
- Multiple servers can be specified in the config file. (`#174
  <https://github.com/MichaelSasser/matrixctl/issues/174>`_)
- Per-server maintenance task configuration. (`#184
  <https://github.com/MichaelSasser/matrixctl/issues/184>`_)
- Optimized startuptime by lazy importing commands by a factor of 10. Added a
  ``addon_manager`` which now manages imports of the addon (sub)parsers. (`#187
  <https://github.com/MichaelSasser/matrixctl/issues/187>`_)
- Add ``get_events`` addon, which gets user-events from the DB. (`#198
  <https://github.com/MichaelSasser/matrixctl/issues/198>`_)
- Add ``reports`` addon. (`#200
  <https://github.com/MichaelSasser/matrixctl/issues/200>`_)
- Add ``report`` addon. (`#202
  <https://github.com/MichaelSasser/matrixctl/issues/202>`_)
- Replace ``tabulate`` with the new ``table`` handler. (`#206
  <https://github.com/MichaelSasser/matrixctl/issues/206>`_)
- With the ``-j`` or ``--to-json`` argument, the output of ``reports``,
  ``rooms``, ``users`` and ``user`` can be set to the JSON format. (`#211
  <https://github.com/MichaelSasser/matrixctl/issues/211>`_)
- All API requests which need multiple requests to collect all data are now
  asynchronous. Add a optional ``[limit]`` argument to the ``users`` and
  ``reports`` addon. (`#217
  <https://github.com/MichaelSasser/matrixctl/issues/217>`_)
- Add (one-pass) Jinja2 support for the configuration file. (`#229
  <https://github.com/MichaelSasser/matrixctl/issues/229>`_)


Miscellaneous
-------------

- Add tests for the yaml handler. (`#174
  <https://github.com/MichaelSasser/matrixctl/issues/174>`_)
- Commands or subcommands are now located in ``matrixctl.commands`` as packages and
  considered commands. Commands are splitted in ``parser.py`` and ``addon.py``. It is
  now allowed to use multible modules for one addon. (`#187
  <https://github.com/MichaelSasser/matrixctl/issues/187>`_)
- More flexible yaml handler. (`#213
  <https://github.com/MichaelSasser/matrixctl/issues/213>`_)


0.10.3 (2021-06-26)
===================

Features & Improvements
-----------------------

- The docks have moved back to (`https://matrixctl.readthedocs.io/
  <https://matrixctl.readthedocs.io/>`_)`. (`#69
  <https://github.com/MichaelSasser/matrixctl/issues/69>`_)


Bugfixes
--------

- Make MatrixCtl compatible with Python 3.8. (`#146
  <https://github.com/MichaelSasser/matrixctl/issues/146>`_)


Improved Documentation
----------------------

- Add Contribution Guidlines (`#149
  <https://github.com/MichaelSasser/matrixctl/issues/149>`_)


Miscellaneous
-------------

- The ``event_id`` of the command ``get-event`` now gets sanitized. (`#143
  <https://github.com/MichaelSasser/matrixctl/issues/143>`_)


0.10.2 (2021-06-24)
===================

Features & Improvements
-----------------------

- Add start/restart switch to the deploy subcommand to start/restart the server
  right after the deployment. (`#132
  <https://github.com/MichaelSasser/matrixctl/issues/132>`_)
- Added the new command ``get-event``, which gets an event by ``event_id`` from
  the Database and prints it as JSON. (`#139
  <https://github.com/MichaelSasser/matrixctl/issues/139>`_)


Miscellaneous
-------------

- Rewritten API handler. (`#136
  <https://github.com/MichaelSasser/matrixctl/issues/136>`_)
- Fixed: Wrong version while developing in virtual environment. (`#141
  <https://github.com/MichaelSasser/matrixctl/issues/141>`_)


0.10.1 (2021-06-17)
===================

Features & Improvements
-----------------------

- Update type hinting according to PEP 585. (`#123
  <https://github.com/MichaelSasser/matrixctl/issues/123>`_)


0.10.0 (2021-06-17)
===================

Behavior & Breaking Changes
---------------------------

- Drop support for Python 3.8 for tests and typing. (`#121
  <https://github.com/MichaelSasser/matrixctl/issues/121>`_)


Features & Improvements
-----------------------

- add ``purge-history`` to purge historic events from the DB (`#86
  <https://github.com/MichaelSasser/matrixctl/issues/86>`_)
- Modules are using ``logger`` instead of ``logging``. (`#117
  <https://github.com/MichaelSasser/matrixctl/issues/117>`_)
- Use secure, temporary directory for ansible_runner's private data. (`#119
  <https://github.com/MichaelSasser/matrixctl/issues/119>`_)


Miscellaneous
-------------

- Moved ``mypy.ini`` into ``pyproject.toml``. (`#113
  <https://github.com/MichaelSasser/matrixctl/issues/113>`_)
- Fix of false-positive ``CWE-798: Use of Hard-coded Credentials``. (`#115
  <https://github.com/MichaelSasser/matrixctl/issues/115>`_)
- Update ``pre-commit`` and dependencies. (`#121
  <https://github.com/MichaelSasser/matrixctl/issues/121>`_)


0.9.0 (2021-04-23)
==================

Behavior & Breaking Changes
---------------------------

- add ``shadow-banned`` (needs synapse v1.28 or greater) and ``displayname`` to
  the table output of ```matrixctl users``. (`#30
  <https://github.com/MichaelSasser/matrixctl/issues/30>`_)


Features & Improvements
-----------------------

- Add the ``stop`` command to ``matrixctl``, which stops all OCI containers.
  (`#74 <https://github.com/MichaelSasser/matrixctl/issues/74>`_)


Improved Documentation
----------------------

- Fixed the commandline tool example in the docs. (`#68
  <https://github.com/MichaelSasser/matrixctl/issues/68>`_)
- Removed the program name from every title of the changelog. We now only use
  the version number and the date. (`#79
  <https://github.com/MichaelSasser/matrixctl/issues/79>`_)


0.8.6 (2021-04-17)
==================

Features & Improvements
-----------------------

- The application now uses ``__main__.py`` instead of ``application.py``.
  Developers are now able to use ``python matrixctl`` from the project root to
  start the application. (`#60
  <https://github.com/MichaelSasser/matrixctl/issues/60>`_)
- Add tox as simple way to check the changelog, testbuild the docs, run
  pre-commit and run tests (`#64
  <https://github.com/MichaelSasser/matrixctl/issues/64>`_)


Bugfixes
--------

- Fix ``TypeError`` when enabling debug mode and using the API. (`#45
  <https://github.com/MichaelSasser/matrixctl/issues/45>`_)


Miscellaneous
-------------

- Add ``CHANGELOG.rst`` to project root generated by ``towncrier``.
  This is the first release using the new changelog generation procedure.
  If you want to see the previous changelog please check our `releases on
  GitHub
  <https://github.com/MichaelSasser/matrixctl/releases>`_. (`#61
  <https://github.com/MichaelSasser/matrixctl/issues/61>`_)


0.8.5 (2021-02-24)
==================

Bugfixes
--------

- Add the new ``serve-notice`` feature.


0.8.4 (2021-02-24)
==================

.. note:: This version of MatrixCtl has not been released.


0.8.3 (2021-02-24)
==================

.. note:: This version of MatrixCtl has not been released.


0.8.2 (2021-02-24)
==================

.. note:: This version of MatrixCtl has not been released.

Features & Improvements
-----------------------

- feature ``upload`` which makes it possible to upload files and images. It returns the ``mxc://`` uri.
- feature ``server-notice``.

Miscellaneous
-------------

- Changed docs to classic python theme.


0.8.1 (2020-12-02)
==================

Behavior & Breaking Changes
---------------------------

- The ``update`` command now uses config: ``[SYNAPSE]`` -> ``Playbook`` instead of ``[SYNAPSE]`` -> ``Path``

Features & Improvements
-----------------------

- Add missing ``[SYNAPSE]`` (config file) documentation.


0.8.0 (2020-12-02)
==================

Behavior & Breaking Changes
---------------------------

- The option to run multiple playbooks with matrixctl. The user should use - import_playbook: /PathTo/matrix-docker-ansible-deploy/setup.yml in an own playbook. (`#20
  <https://github.com/MichaelSasser/matrixctl/issues/20>`_)(`#21
  <https://github.com/MichaelSasser/matrixctl/issues/21>`_)

Features & Improvements
-----------------------

- The ``ansible`` handler now uses ``ansible-runner`` instead of ``subprocess`` (`#20
  <https://github.com/MichaelSasser/matrixctl/issues/20>`_)(`#21
  <https://github.com/MichaelSasser/matrixctl/issues/21>`_)
- The ``api`` handler now gives the user a hint, when the admin api is disabled.


0.7.0 (2020-09-25)
==================

Behavior & Breaking Changes
---------------------------

- Removed the ``--with-bots``, "bots" are now shown by default (`#15
  <https://github.com/MichaelSasser/matrixctl/issues/15>`_)

Bugfixes
--------

- Fixed the deploy control logic (`#18
  <https://github.com/MichaelSasser/matrixctl/issues/18>`_)


0.6.3 (2020-09-17)
==================

Features & Improvements
-----------------------

- With the help of two args it is possible to deploy the two playbooks independently:
  - ``-s``/``--synapse``: Only deploy the synapse playbook,
  - ``-a``/``--ansible``: Only deploy your own playbook.


0.6.2 (2020-09-16)
==================

Bugfixes
--------

- It is now possible to deploy, when only one of ``[ANSIBLE]`` or ``[SYNAPSE]`` are configured.


0.6.1 (2020-06-02)
==================

Features & Improvements
-----------------------

- If the access-token has changed or is wrong, MatrixCtl now throws a specific error, which tells the user, what went wrong. (`#12
  <https://github.com/MichaelSasser/matrixctl/issues/12>`_)
- Replace the assertions from the API handler with proper ``TypeError``.


0.6.0 (2020-05-12)
==================

Behavior & Breaking Changes
---------------------------

- Changed ``users --no-bots`` or ``users -b`` to ``users --with-bots`` or ``users -b``
- Changed ``users --guests`` or ``users -g`` to ``users --with-guests`` or ``users -g``

Features & Improvements
-----------------------

- ``users --with-deactivated`` or ``users -d`` (`#2
  <https://github.com/MichaelSasser/matrixctl/issues/2>`_)

Bugfixes
--------

- SSH handler logs an error if unable to connect (`#7
  <https://github.com/MichaelSasser/matrixctl/issues/7>`_)


0.5.0 (2020-04-30)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

Behavior & Breaking Changes
---------------------------

- Fixed typo in the ``maintenance`` command.

Removals & Deprecations
-----------------------

- Removed ``run-postgres-synapse-janitor`` from maintenance because it may destroy the DB (`#8
  <https://github.com/MichaelSasser/matrixctl/issues/8>`_)(`#465 (spantaleev/matrix-docker-ansible-deploy)
  <https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/465>`_)


0.4.0 (2020-04-22)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

Behavior & Breaking Changes
---------------------------

- ``rooms`` submodule: Changed argument ``--order_by_size`` to
  ``--order-by-size``.

Features & Improvements
-----------------------

- Add the ``version`` command.
- Add the ``delroom`` command.
- Add more debug output to the API handler (``params``, ``data``, ``method`` and censored
  ``headers``)


0.3.2 (2020-04-21)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

Features & Improvements
-----------------------

- Add the ``rooms`` command.


0.3.1 (2020-04-21)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

.. note:: This version of MatrixCtl has not been released.


0.3.0 (2020-04-20)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

.. note:: No significant changes to the Project.

Project restructured.


0.2.2 (2020-04-13)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

Features & Improvements
-----------------------

- Added docs to the Project (``gh-pages`` branch).

Bugfixes
--------

- ``matixctl adduser --ansible``. MatrixCtl was not able to create a user with the ``--ansible`` argument.


0.2.1 (2020-04-13)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

.. note:: This version of MatrixCtl has not been released.


0.2.0 (2020-04-12)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

Behavior & Breaking Changes
---------------------------

- The command ``list-user`` has been renamed to ``users``.

Features & Improvements
-----------------------

- Add the command ``user``.


0.1.4 (2020-04-10)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

Features & Improvements
-----------------------

- Add the command ``start``.
- Add the command ``restart`` (alias for ``start``).
- Add the command ``check``.


0.1.3 (2020-04-10)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

Features & Improvements
-----------------------

- Add the command ``adduser-jitsi``.
- Add the command ``deluser-jitsi``.


0.1.2 (2020-04-07)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

**First official release.**

Features & Improvements
-----------------------

- Add the command ``list-users``.


0.1.1 (2020-04-07)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!


.. note:: No significant changes to the Project.


Trivial Changes
---------------

- Fixed GitHub Wokflow.


0.1.0 (2020-04-07)
==================

.. warning:: Since the ``synapse-janitor`` is not safe to use anymore, please
             **do not** use the ``maintenance`` command for any MatrixCtl
             version below 0.5.0!

.. note:: No significant changes to the Project.

**Internal Release**
