# Opens an SFTP session and downloads two types of files from the Probe Hosts — .rules
# files which define how incoming alerts are matched, suppressed and deduplicated, and lookup files which are used to enrich
# alerts with additional context. Saves each file under output_dir and returns metadata
# (type, filename, local path) for every file pulled.

import os           # Local file/folder handling
import socket       # Used to open the TCP connection with an explicit timeout
import paramiko     # SSH/SFTP library
import logging      # Logging

logger = logging.getLogger(__name__)    # Logging for this file

def connect_to_probe_hosts(host, key_path, output_dir, port=22, username='netcool', last_extraction_date=None, connect_timeout=10):
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

        for tag, remote_dir, filenames in (('rules', rules_path, rules_files), ('lookup', lookup_path, lookup_files)):
            local_dir = os.path.join(output_dir, 'probe_hosts', tag)
            os.makedirs(local_dir, exist_ok=True)
            for f in filenames:
                local_path = os.path.join(local_dir, f)
                sftp.get(f'{remote_dir}/{f}', local_path)
                files_pulled.append({'type': tag, 'filename': f, 'local_path': local_path})

        logger.info(f"Probe Hosts extraction complete - {len(files_pulled)} files pulled")
        sftp.close()
        transport.close()
        return files_pulled

    except Exception as e:
        logger.error(f"Probe hosts extraction failed - {e}")
        return None