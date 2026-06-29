## PROBE HOSTS

import logging      # Logging

logger = logging.getLogger(__name__)    # Logging for this file

def connect_to_probe_hosts(client, last_extraction_date=None):
    try:
        # Opens a SFTP sesssion using the bastion session (client) and creates an
        # empty list that we'll add each file we pull to.
        sftp = client.open_sftp()
        logger.info("Probe hosts SFTP connection established")
        files_pulled = []

        if last_extraction_date is None:
            rules_files = sftp.listdir('...')        ## Replace with actual directory.
            lookup_files = sftp.listdir('...')  
        else:
            # Pulls files based on if the modified time of the file is after the last extraction date.
            rules_files = [f for f in sftp.listdir('...') if sftp.stat(f'...{f}').st_mtime >= last_extraction_date]
            lookup_files = [f for f in sftp.listdir('...') if sftp.stat(f'...{f}').st_mtime >= last_extraction_date]

        # Loops through each rules file found and appends it to files_pulled list.
        # Tags it as 'rules'.
        for f in rules_files:
            files_pulled.append(('rules', f))

        # Loops through each lookup file found and appends it to files_pulled list.
        # Tags it as 'lookup'.
        for f in lookup_files:
            files_pulled.append(('lookup', f))

        logger.info(f"Probe Hosts extraction complete - {len(files_pulled)} files pulled")
        sftp.close()
        return files_pulled
    
    except Exception as e:
        logger.error(f"Probe hosts extraction failed - {e}")
        return None