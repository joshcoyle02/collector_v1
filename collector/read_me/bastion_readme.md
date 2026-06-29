## BASTION.PY CONTEXT ##

The bastion is responsible for connecting the collector to Netcool.

### def connect_to_bastion(hostname, username, key_path, port=22):

        hostname    →  the Bastion's IP address
        username    →  who we're connecting as
        key_path    →  where the private key file lives on the machine
        port=22     →  the SSH port, defaults to 22 unless told otherwise