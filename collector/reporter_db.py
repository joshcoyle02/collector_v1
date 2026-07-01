# Opens a PostgreSQL connection to Reporter DB (via the Bastion tunnel) and queries the
# reporter_status table to extract historical event data including volumes, sources and severity.
# On the first run it pulls everything, on subsequent runs it only pulls records modified since
# the last extraction to avoid duplicates. Returns the query results as structured rows of data.

import psycopg2     # PostgreSQL library
import logging      # Logging

logger = logging.getLogger(__name__)    # Logger for this file


# host = IP passed in from collector.py
# port = 5432
# user = db_user passed in
# password = db_password passed in
# dbname = db_name passed in (netcool_mock)


def connect_to_reporter_db(host, port, db_user, db_password, db_name, last_extraction_date=None):               #→  opens the PostgreSQL connection
    try:
        connection = psycopg2.connect(host=host, port=port, user=db_user, password=db_password, dbname=db_name)
        cursor = connection.cursor()    # tool for running SQL queries
        logger.info("Reporter DB connection established")

        if last_extraction_date is None:
            query = "SELECT * FROM reporter_status"
        else:
            query = f"SELECT * FROM reporter_status WHERE last_modified >= '{last_extraction_date}'"

        cursor.execute(query)
        columns = [col.name for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        logger.info(f"Reporter DB extraction complete -{len(results)} records pulled")

        cursor.close()
        connection.close()
        return results
    
    except Exception as e:
        logger.error("Reporter DB extraction failed - {e}")
        return None

