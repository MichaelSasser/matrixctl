.. code-block:: yaml
   :linenos:

   # Define your homeservers in "servers" here.
   servers:
       # Your default server. You can specify muliple servers here with arbitrary
       # Names
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
       # provision your Server without this section. You also can create a user with
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
         token: "MyMatrixToken"

         # In some cases, MatrixCtl does need to make many requests. To speed those
         # requests a notch, you can set a concurrent_limit which is greater than
         # one. This sets a limit to how many asynchronous workers can be spawned
         # by MatrixCtl. If you set the number to high, MatrixCtl needs more time
         # to spawn the workers, then a synchronous request would take.
         concurrent_limit: 10

       # Here you can add your SSH configuration.
       ssh:
         address: matrix.example.com

         # The default port is 22
         port: 22

         # The default username is your current login name.
         user: john

       # Define your maintenance tasks
       maintenance:
         tasks:
           - compress-state  # Compress synapses state table
           - vacuum          # VACUUM the synapse database (garbage-collection)

       # Add connection parameters to the Database
       # Synapse does only read (SELECT) information from the database.
       # The user needs to be able to login to the synapse database
       # and SELECT from the events and event_json tables.
       database:
         synapse_database: synapse  # this is the playbooks default table name
         synapse_user: matrixctl    # the username (role) for the database
         synapse_password: "RolePassword"
         tunnel: true        # true if an ssh tunnel should be used to connect

         # The port that was used in the playbook  (e.g.
         # matrix_postgres_container_postgres_bind_port: 5432)
         # or for your external database. For security reasons the port
         # should be blocked by your firewall. Iy you enable the tunnel
         # by setting tunnel: true, MatrixCtl activates a SSH tunnel.
         port: 5432          # the remote port

     # Another server.
     foo:
       # ...
