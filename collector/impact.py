## IMPACT

import logging      #Logging

logger = logging.getLogger(__name__)

def connect_to_impact(client, last_extraction_date=None):
    try:
        sftp = client.open_sftp()
        logger.info("Impact SFTP connection established")
        files_pulled = []

        impact_path = None     # Path to enrichment files.  Will be updated with actual Netcool path.

        if last_extraction_date is None:
            policy_files = sftp.listdir(impact_path)    # Pulls all files.
        else:
            # Pulls files modified since the last extraction date.
            policy_files = [f for f in sftp.listdir(impact_path) if sftp.stat(f'{impact_path}/{f}').st_mtime >= last_extraction_date]
        
        for f in policy_files:
            files_pulled.append(('policy', f))
        
        logger.info(f"Impact extraction complete - {len(files_pulled)} files pulled.")
        sftp.close()
        return files_pulled

    except Exception as e:
        logger.error(f"Impact extraction failed - {e}")
        return None