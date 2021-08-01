.. code-block:: yaml
   :linenos:

   # Your default server. You can specify muliple servers.
   default:

     ansible:
       # The absolute path to your playbook
       playbook: /path/to/ansible/playbook

     synapse:
       # The absolute path to the synapse playbook.
       # This is only used for updating the playbook.
       playbook: /path/to/synapse/playbook

     # If your matrix server is deployed, you may want to fill out the API section.
     # It enables matrixctl to run more and faster commands. You can deploy and
     # provision your Server without this section. You also can cerate a user with
     # "matrixctl adduser --ansible YourUsername" and add your privileges after
     # that.
     api:
       # Your domain should be something like "michaelsasser.org" without the
       # "matrix." in the front. MatrixCtl will add that, if needed. An IP-Address
       # is not enough.
       domain: example.com

       # The username your admin user
       username: johndoe

       # To use the API you need to have an administrator account. Enter your Token
       # here. If you use the element client you will find it your user settings
       # (click on your username on the upper left corner on your browser) in the
       # "Help & About" tab. If you scroll down click next to "Access-Token:" on
       # "<click to reveal>". It will be marked for you. Copy it in here.
       token= "MyMatrixToken"

     # Here you can add your SSH configuration.
     ssh:
       address: matrix.example.com

       # The default port is 22
       port: 22

       # The default username is your current login name.
       user: john

   # Another server.
   foo:
     # ...
