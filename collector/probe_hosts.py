# Opens an SFTP session and pulls two types of files from the Probe Hosts — .rules 
# files which define how incoming alerts are matched, suppressed and deduplicated, and lookup files which are used to enrich 
# alerts with additional context. Returns a list of all pulled files tagged as either 'rules' or 'lookup'.

import socket       # Used to open the TCP connection with an explicit timeout
import paramiko     # SSH/SFTP library
import logging      # Logging

logger = logging.getLogger(__name__)    # Logging for this file

def connect_to_probe_hosts(host, key_path, port=22, username='netcool', last_extraction_date=None, connect_timeout=10):
    try:
        # Opens a direct SFTP connection to Probe Hosts
        # A pre-connected, timed-out socket is used instead of paramiko.Transport((host, port))
        # because that path has no timeout and hangs on the OS default if the port is filtered.
        sock = socket.create_connection((host, port), timeout=connect_timeout)
        transport = paramiko.Transport(sock)
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        transport.connect(username=username, pkey=private_key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        logger.info(f"Probe Hosts SFTP connection established - {host}:{port}")
        files_pulled = []

        rules_path = '/opt/IBM/tivoli/netcool/omnibus/probes'
        lookup_path = '/opt/IBM/tivoli/netcool/omnibus/probes'     # To be confirmed

        if last_extraction_date is None:
            rules_files = sftp.listdir(rules_path)
            lookup_files = sftp.listdir(lookup_path)
        else:
            rules_files = [f for f in sftp.listdir(rules_path) if sftp.stat(f'{rules_path}/{f}').st_mtime >= last_extraction_date]
            lookup_files = [f for f in sftp.listdir(lookup_path) if sftp.stat(f'{lookup_path}/{f}').st_mtime >= last_extraction_date]

        for f in rules_files:
            files_pulled.append(('rules', f))

        for f in lookup_files:
            files_pulled.append(('lookup', f))

        logger.info(f"Probe Hosts extraction complete - {len(files_pulled)} files pulled")
        sftp.close()
        transport.close()
        return files_pulled
    
    except Exception as e:
        logger.error(f"Probe hosts extraction failed - {e}")
        return None