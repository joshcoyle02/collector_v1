import paramiko     # Python library that supports SSH connections.
import logging      # Pythons logging library

logger = logging.getLogger(__name__)    # Tool for logging.

def connect_to_bastion(hostname, username, key_path, port=22):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    # Auto run on unrecognised server.
        private_key = paramiko.RSAKey.from_private_key_file(key_path)   # Pulls key from the key file.
        client.connect(hostname=hostname, username=username, pkey=private_key, port=port)   # Makes the connection.
        logger.info(f"Bastion connection established = {hostname}")     # Logs sucessful connection
        return client
    
    except Exception as e:
        logger.error(f"Bastion connection failed = {e}")     # Logs unsucessful connection
        return None
