# Opens a raw TCP connection to ObjectServer on port 4100 and sends SQL queries
# to extract live active alerts and automation rules. No credentials needed.
# Returns the query results as structured data.

import socket       # Python built in library for raw TCP connections
import logging      # Logging

logger = logging.getLogger(__name__)    # Logger for this file

COLUMNS = [
    "Identifier", "Serial", "Node", "NodeAlias", "Manager", "Agent",
    "AlertGroup", "AlertKey", "Severity", "Summary", "StateChange",
    "FirstOccurrence", "LastOccurrence", "Tally", "Class", "Type",
    "Acknowledged", "EventId", "Customer", "Service", "ServerName", "ServerSerial"
]

def connect_to_object_server(host, port=4100, last_extraction_date=None, recv_timeout=10):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.settimeout(recv_timeout)
        logger.info(f"ObjectServer connection established - {host}:{port}")

        column_list = ",".join(COLUMNS)
        if last_extraction_date is None:
            query = f"select {column_list} from alerts.status;\n"
        else:
            query = f"select {column_list} from alerts.status where LastOccurrence >= '{last_extraction_date}';\n"

        sock.sendall(query.encode())

        # ObjectServer doesn't signal end-of-response, so keep reading until
        # the socket goes quiet (rather than a single recv(), which silently
        # truncates once a response spans more than one packet/buffer).
        chunks = []
        try:
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
        except socket.timeout:
            pass

        sock.close()

        results = []
        for line in b"".join(chunks).decode().splitlines():
            if not line.strip():
                continue
            results.append(dict(zip(COLUMNS, line.split(","))))

        logger.info(f"ObjectServer extraction complete - {len(results)} records pulled")
        return results

    except Exception as e:
        logger.error(f"ObjectServer extraction failed - {e}")
        return None