# Combines all the collector functions into one singular function "run_extraction".
# host is a required argument - pass "localhost" if the collector runs on the same
# host as the mock, or the Netcool host's IP if it's running elsewhere with a direct route.

import logging
from collector.reporter_db import connect_to_reporter_db
from collector.object_server import connect_to_object_server
from collector.probe_hosts import connect_to_probe_hosts
from collector.impact import connect_to_impact

logger = logging.getLogger(__name__)

def run_extraction(netcool_host, key_path, db_user, db_password, db_name,
                    reporter_db_port=5432, object_server_port=4100, sftp_port=22,
                    last_extraction_date=None):
    try:
        reporter_db_results = connect_to_reporter_db(
            host=netcool_host,
            port=reporter_db_port,
            db_user=db_user,
            db_password=db_password,
            db_name=db_name,
            last_extraction_date=last_extraction_date
        )

        object_server_results = connect_to_object_server(
            host=netcool_host,
            port=object_server_port,
            last_extraction_date=last_extraction_date
        )

        probe_hosts_results = connect_to_probe_hosts(
            host=netcool_host,
            port=sftp_port,
            key_path=key_path,
            last_extraction_date=last_extraction_date
        )

        impact_results = connect_to_impact(
            host=netcool_host,
            port=sftp_port,
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
