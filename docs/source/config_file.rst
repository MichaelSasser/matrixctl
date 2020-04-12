To use this program you need to have this config file in
`/etc/matrixctl/config` or in `~/.config/matrixctl/config`.

.. code-block:: toml
   :linenos:

   [ANSIBLE]
   # The absolute path to the fully configured matrix-docker-ansible-deploy
   # playbook from https://github.com/spantaleev/matrix-docker-ansible-deploy.

   MatrixDockerAnsibleDeployPath="/absolut/path/to/matrix-docker-ansible-deploy"

   [SERVER]
   # If you have your own playbook, to provision your matrix server, you can
   # fill out this section. MatrixCtl will run this before the
   # matrix-docker-ansible-deploy playbook.

   # If you have a special "ansible.cfg" for your playbook, fill in the absolute
   # path to it.

   # AnsibleCfg="/absolute/path/to/ansible.cfg"

   # Fill in the absolute path to your "site.yml"

   # AnsiblePlaybook="/absolute/path/to/site.yml"

   # If you use tags to provision or configure your matrix host, you can add them
   # here. Use a comma separated string without spaces.

   # AnsibleTags="MyTag,MyOtherTag"

   [API]
   # If your matrix server is deployed, you may want to fill out the API section.
   # It enables matrixctl to run more and faster commands. You can deploy and
   # provision your Server without this section. You also can cerate a user with
   # "matrixctl adduser --ansible YourUsername" and add your privileges after
   # that.

   # Your domain should be something like "michaelsasser.org" without the
   # "matrix." in the front. MatrixCtl will add that, if needed. An IP-Address
   # is not enough.

   # Domain="domain.tld"

   # To use the API you need to have an administrator account. Enter your Token
   # here. If you use the riot client you will find it your user settings (click
   # on your username on the upper left corner on your browser) in the
   # "Help & About" tab. If you scroll down click next to "Access-Token:" on
   # "<click to reveal>". It will be marked for you. Copy it in here.

   # Token="MyMatrixToken"
