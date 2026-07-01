# Combines all the collector functions into one singular function "run_extraction".
# No bastion or tunnel needed — the collector runs on the same host as the mock,
# so all components connect directly to localhost.

import logging
from collector.reporter_db import connect_to_reporter_db
from collector.object_server import connect_to_object_server
from collector.probe_hosts import connect_to_probe_hosts
from collector.impact import connect_to_impact

logger = logging.getLogger(__name__)

def run_extraction(db_user, db_password, db_name, last_extraction_date=None):
    try:
        reporter_db_results = connect_to_reporter_db(
            host="localhost",
            port=5432,
            db_user=db_user,
            db_password=db_password,
            db_name=db_name,
            last_extraction_date=last_extraction_date
        )

        object_server_results = connect_to_object_server(
            host="localhost",
            last_extraction_date=last_extraction_date
        )

        probe_hosts_results = connect_to_probe_hosts(
            host="localhost",
            key_path=key_path,
            last_extraction_date=last_extraction_date
        )

        impact_results = connect_to_impact(
            host="localhost",
            key_path=key_path,
            last_extraction_date=last_extraction_date
        )

        logger.info("Reporter DB extraction - %s", 'success' if reporter_db_results is not None else 'failed')
        logger.info("ObjectServer extraction - %s", 'success' if object_server_results is not None else 'failed')
        logger.info("Probe Hosts extraction - %s", 'success' if probe_hosts_results is not None else 'failed')
        logger.info("Impact extraction - %s", 'success' if impact_results is not None else 'failed')

        return {
            "reporter_db": reporter_db_results,
            "object_server": object_server_results,
            "probe_hosts": probe_hosts_results,
            "impact": impact_results
        }

    except Exception as e:
        logger.error("Extraction failed - %s", e)
        return None
