# Opens an SFTP session and pulls enrichment policy files from the Netcool/Impact server.
# These are files that define how alerts get enriched with business context, for example SAP lookups. 
# Returns a list of the pulled files tagged as 'policy'.

import paramiko     # SSH/SFTP library
import logging      # Logging

logger = logging.getLogger(__name__)    # Logging for this file

def connect_to_impact(host, key_path, port=22, username='netcool', last_extraction_date=None):
    try:
        # Opens a direct SFTP connection to Impact
        transport = paramiko.Transport((host, port))
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

        for f in policy_files:
            files_pulled.append(('policy', f))

        logger.info(f"Impact extraction complete - {len(files_pulled)} files pulled")
        sftp.close()
        transport.close()
        return files_pulled

    except Exception as e:
        logger.error(f"Impact extraction failed - {e}")
        return None