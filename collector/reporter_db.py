# Opens a JDBC connection to the Reporter DB and queries the events table to extract historical event data including volumes, 
# sources and severity.Opens a JDBC connection to the Reporter DB and queries the events table to extract historical event
# data including volumes, sources and severity. On the first run it pulls everything, on subsequent runs it only pulls records 
# modified since the last extraction to avoid duplicates. Returns the query results as structured rows of data.

## IMPORTANT ##
# Have to implement the connection to the tunnel created in client. 
# JDBC is tricky, do this when a test instance has been created.

import jaydebeapi   # Python library allows to connect to databases using JDBC
import logging      # Logging

logger = logging.getLogger(__name__)    ## Logger for this file

def connect_to_reporter_db(client, jdbc_url, db_user, db_password, jar_path, last_extraction_date=None):
    try:
        connection = jaydebeapi.connect("com.ibm.db2.jcc.DB2Driver", jdbc_url, [db_user, db_password], jar_path)
        cursor = connection.cursor()                        # For writing SQL queries against the databse.
        logger.info("Reporter DB connection established.")

        if last_extraction_date is None:

            # REPORTER.EVENTS is a placeholder table name, replace with actual netcool table name.  Same with LASTMODIFIED.
            query = "SELECT * FROM REPORTER.EVENTS"     # Subject to change on implementation.  Pulls event data.
        else:

            # Only pulls records modified since the last extraction.  No duplicates.
            query = f"SELECT * FROM REPORTER.EVENTS WHERE LASTMODIFIED >= '{last_extraction_date}'"

        # Runs SQL query from the IF statement and stores it in results.
        cursor.execute(query)
        results = cursor.fetchall()
        logger.info(f"Reporter DB extraction complete - {len(results)} pulled.")

        cursor.close()      # Closes cursor.
        connection.close()  # Closes the JDBC connection.
        return results
    
    except Exception as e:
        logger.error(f"Reporter DB extraction failed - {e}")
        return None