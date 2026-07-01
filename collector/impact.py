# Opens an SFTP session and downloads enrichment policy files from the Netcool/Impact server.
# These are files that define how alerts get enriched with business context, for example SAP lookups.
# Saves each file under output_dir and returns metadata (type, filename, local path) for every file pulled.

import os           # Local file/folder handling
import socket       # Used to open the TCP connection with an explicit timeout
import paramiko     # SSH/SFTP library
import logging      # Logging

logger = logging.getLogger(__name__)    # Logging for this file

def connect_to_impact(host, key_path, output_dir, port=22, username='netcool', last_extraction_date=None, connect_timeout=10):
    try:
        # Opens a direct SFTP connection to Impact
        # A pre-connected, timed-out socket is used instead of paramiko.Transport((host, port))
        # because that path has no timeout and hangs on the OS default if the port is filtered.
        sock = socket.create_connection((host, port), timeout=connect_timeout)
        transport = paramiko.Transport(sock)
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        transport.connect(username=username, pkey=private_key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        logger.info(f"Impact SFTP connection established - {host}:{port}")
        files_pulled = []

        impact_path = '/opt/IBM/tivoli/netcool/impact/policy'      # From handover doc

        if last_extraction_date is None:
            policy_files = sftp.listdir(impact_path)
        else:
            policy_files = [f for f in sftp.listdir(impact_path) if sftp.stat(f'{impact_path}/{f}').st_mtime >= last_extraction_date]

        local_dir = os.path.join(output_dir, 'impact', 'policy')
        os.makedirs(local_dir, exist_ok=True)
        for f in policy_files:
            local_path = os.path.join(local_dir, f)
            sftp.get(f'{impact_path}/{f}', local_path)
            files_pulled.append({'type': 'policy', 'filename': f, 'local_path': local_path})

        logger.info(f"Impact extraction complete - {len(files_pulled)} files pulled")
        sftp.close()
        transport.close()
        return files_pulled

    except Exception as e:
        logger.error(f"Impact extraction failed - {e}")
        return None