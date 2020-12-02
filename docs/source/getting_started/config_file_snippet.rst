.. code-block:: toml
   :linenos:

   [ANSIBLE]
   # The absolute path to your playbook
   #
   # Playbook = "/absolute/path/to/your/playbook"

   [API]
   # If your matrix server is deployed, you may want to fill out the API section.
   # It enables matrixctl to run more and faster commands. You can deploy and
   # provision your Server without this section. You also can cerate a user with
   # "matrixctl adduser --ansible YourUsername" and add your privileges after
   # that.

   # Your domain should be something like "michaelsasser.org" without the
   # "matrix." in the front. MatrixCtl will add that, if needed. An IP-Address
   # is not enough.
   #
   # Domain="domain.tld"

   # To use the API you need to have an administrator account. Enter your Token
   # here. If you use the riot client you will find it your user settings (click
   # on your username on the upper left corner on your browser) in the
   # "Help & About" tab. If you scroll down click next to "Access-Token:" on
   # "<click to reveal>". It will be marked for you. Copy it in here.
   #
   # Token="MySuperLongMatrixToken"

   [SSH]
   # Here you can add your SSH configuration.
   #
   # Address = "matrix.domain.tld"

   # The default port is 22
   #
   # Port = 22

   # The default username is your current login name.
   #
   # User = "myusername"
