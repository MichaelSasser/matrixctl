SSH Public Key
**************

To get easy access to the other matrix plugins (e.g. bridges) and other
additional functionality, to communicate with the OCI containers, you need to
have a ssh public key installed on your matrix host server.
We user ssh access for the following:

- ``matrixctl adduser-jitsi``
- ``matrixctl deluser-jitsi``


.. note:: If you where alreadey able to ran the
          `spantaleev/matrix-docker-ansible-deploy <https://github.com/spantaleev/matrix-docker-ansible-deploy>`_
          playbook, you have installed the public key before. You are good
          to go and you can skip this chapter.

.. note:: To get your public key installd you can use your own playbook like
          described in :ref:`Config File` chapter under the ``[SERVER]``
          section. If you don't want to write your own playbook, follow this
          guide.

Check your key pair
-------------------

Check, if you alreadey have a key pair.

.. code-block:: console

   $ ls -la ~/.ssh/id_*.pub
   -rw-r--r-- 1 michael users 767 30. Sep 2014  /home/michael/.ssh/id_rsa.pub

If the output looks like the above, you have generated a keypare in the past
and you can continue in the next section :ref:`Copy Public Key`.

If it looks something like below or prints something like you can continue in
the section: :ref:`Generate key pair`.

.. code-block:: console

   $ ls -la ~/.ssh/id_*.pub
   zsh: no matches found: /home/michael/.ssh/id_*.pub
   # or
   $ ls -la ~/.ssh/id_*.pub
   ls: cannot access '/home/michael/.ssh/id_*.pub': No such file or directory

Generate key pair
-----------------

To generate your key pair run:

.. code-block:: console

   $ mkdir ~/.ssh
   $ ssh-keygen -t rsa -b 4096 -C "your_email@domain.tld"
   Generating public/private rsa key pair.
   Enter file in which to save the key (/root/.ssh/id_rsa):
   Created directory '/root/.ssh'.
   Enter passphrase (empty for no passphrase):
   Enter same passphrase again:
   Your identification has been saved in /root/.ssh/id_rsa
   Your public key has been saved in /root/.ssh/id_rsa.pub
   The key fingerprint is:
   SHA256:UjqL4jzmuk2YjVqzVHNIay2TShDss5wMHyq3V7ZlI1M your_email@domain.tld
   The key's randomart image is:
   +---[RSA 4096]----+
   |o                |
   | o               |
   |o   .   .        |
   |.+.. = oE        |
   |+o=.X *.S        |
   |o@o+ *=++        |
   |=.O..o.* .       |
   |.B++. .          |
   |+=*o             |
   +----[SHA256]-----+

If prints something like below you need to install ``openssh``, ``sshd`` or
``openssh-client`` (depends on your distribution).

.. code-block:: console

   $ mkdir ~/.ssh
   $ ssh-keygen -t rsa -b 4096 -C "your_email@domain.tld"
   bash: ssh-keygen: command not found

On Arch linux the installation of ``openssl`` would look like:


.. code-block:: console

   $ pacman -Sy openssh
   :: Synchronizing package databases...
    core is up to date
    extra is up to date
    community is up to date
   resolving dependencies...
   looking for conflicting packages...

   Packages (4) dnssec-anchors-20190629-2  ldns-1.7.1-2  libedit-20191231_3.1-1  openssh-8.2p1-3

   Total Download Size:   1.40 MiB
   Total Installed Size:  7.31 MiB

   :: Proceed with installation? [Y/n] y
   :: Retrieving packages...
    libedit-20191231_3.1-1-x86_64         106.9 KiB   656 KiB/s 00:00 [#####################################] 100%
    dnssec-anchors-20190629-2-any           3.1 KiB  0.00   B/s 00:00 [#####################################] 100%
    ldns-1.7.1-2-x86_64                   435.9 KiB   895 KiB/s 00:00 [#####################################] 100%
    openssh-8.2p1-3-x86_64                884.7 KiB  1355 KiB/s 00:01 [#####################################] 100%
   (4/4) checking keys in keyring                                     [#####################################] 100%
   (4/4) checking package integrity                                   [#####################################] 100%
   (4/4) loading package files                                        [#####################################] 100%
   (4/4) checking for file conflicts                                  [#####################################] 100%
   (4/4) checking available disk space                                [#####################################] 100%
   :: Processing package changes...
   (1/4) installing libedit                                           [#####################################] 100%
   (2/4) installing dnssec-anchors                                    [#####################################] 100%
   (3/4) installing ldns                                              [#####################################] 100%
   Optional dependencies for ldns
       libpcap: ldns-dpa tool [installed]
   (4/4) installing openssh                                           [#####################################] 100%
   Optional dependencies for openssh
       xorg-xauth: X11 forwarding
       x11-ssh-askpass: input passphrase in X
       libfido2: FIDO/U2F support
   :: Running post-transaction hooks...
   (1/4) Reloading system manager configuration...
    Skipped: Current root is not booted.
    (2/4) Creating temporary files...
   [/usr/lib/tmpfiles.d/journal-nocow.conf:26] Failed to resolve specifier: uninitialized /etc detected, skipping
   All rules containing unresolvable specifiers will be skipped.
   (3/4) Arming ConditionNeedsUpdate...
   (4/4) Cleaning up package cache...

Copy Public Key
---------------

Now copy your public key to your Server:

.. code-block:: console

   $ ssh-copy-id -i ~/.ssh/id_rsa.pub user@matrix.domain.tld
