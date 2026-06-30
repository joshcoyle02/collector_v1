# Combines all the functions into one singular function "run_extraction".
# Returns the results from each function to its own variable.



import logging                                                  # Logging
from collector.bastion import connect_to_bastion                # Bastion function
from collector.reporter_db import connect_to_reporter_db        # Reporter DB function
from collector.object_server import connect_to_object_server    # ObjectServer function
from collector.probe_hosts import connect_to_probe_hosts        # Probe Hosts function
from collector.impact import connect_to_impact                  # Impact function

logger = logging.getLogger(__name__)    # Logger for this file.

def run_extraction(hostname, username, object_server_host, key_path, jdbc_url, db_user, db_password, jar_path, last_extraction_date=None):
    try:
        client = connect_to_bastion(hostname, username, key_path)       # Calls bastion connection function from bastion.py
        if client is None:
            logger.error("Bastion connection failed - aborting extraction")
            return None
        
        # Calls reporter_db function from reporter_db.py
        reporter_db_results = connect_to_reporter_db(client, jdbc_url, db_user, db_password, jar_path, last_extraction_date)    

        #Calls object_server function from object_server.py
        object_server_results = connect_to_object_server(client, object_server_host, db_user, db_password, last_extraction_date)

        #Calls probe_hosts function from probe_hosts.py
        probe_hosts_results = connect_to_probe_hosts(client, last_extraction_date)

        #Calls impact function from impact.py
        impact_results = connect_to_impact(client, last_extraction_date)

        # Extraction runs logging.
        logger.info(f"Reporter DB extraction - {'success' if reporter_db_results is not None else 'failed'}")
        logger.info(f"ObjectServer extraction - {'success' if object_server_results is not None else 'failed'}")
        logger.info(f"Probe Hosts extraction - {'success' if probe_hosts_results is not None else 'failed'}")
        logger.info(f"Impact extraction - {'success' if impact_results is not None else 'failed'}")

        # Closes the bastion.  Logs that it was closed.  Sends all data extracted back to main.py to be packaged.
        client.close()
        logger.info("Bastion session closed")
        return {
            "reporter_db": reporter_db_results,
            "object_server": object_server_results,
            "probe_hosts": probe_hosts_results,
            "impact": impact_results
        }
    
    except Exception as e:
        logger.error(f"Extraction failed - {e}")
        if client:
            client.close()
            logger.info("Bastion session closed")
        return None