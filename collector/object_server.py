# Opens a raw TCP connection to ObjectServer on port 4100 and sends SQL queries
# to extract live active alerts and automation rules. No credentials needed.
# Returns the query results as structured data.

import socket       # Python built in library for raw TCP connections
import logging      # Logging

logger = logging.getLogger(__name__)    # Logger for this file

def connect_to_object_server(host, port=4100, last_extraction_date=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        logger.info(f"ObjectServer connection established - {host}:{port}")

        if last_extraction_date is None:
            query = "select Node,Severity,Summary from alerts.status;\n"
        else:
            query = f"select Node,Severity,Summary from alerts.status where LastOccurrence >= '{last_extraction_date}';\n"

        sock.sendall(query.encode())
        response = sock.recv(4096)
        results = response.decode()
        logger.info(f"ObjectServer extraction complete - {len(results.splitlines())} records pulled")
        sock.close()
        return results

    except Exception as e:
        logger.error(f"ObjectServer extraction failed - {e}")
        return None