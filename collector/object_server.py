# Opens a SQL connection to the ObjectServer (NCOMS_P) on port 4100 through the Bastion and queries the 
# ALERTS.STATUS table to extract live active alerts and automation rules — including triggers, escalation rules and correlation rules. 
# Returns the query results as structured rows of data.

import logging
import pymysql
logger = logging.getLogger(__name__)

def connect_to_object_server(client, db_user, db_password, last_extraction_date=None):
    try:
        # Opens a SQL connection to Object Server
        connection = pymysql.connect(host='127.0.0.1', port=4100, user=db_user, password=db_password)
        cursor = connection.cursor()
        logger.info("ObjectServer connection established")

        # Pulls alert data from DB.  Checks if this is the first extraction.
        if last_extraction_date is None:
            query = "SELECT * FROM ALERTS.STATUS"
        else:
            query = f"SELECT * FROM ALERTS.STATUS WHERE LastOccurence >= '{last_extraction_date}'"

        cursor.execute(query)
        results = cursor.fetchall()
        logger.info(f"ObjectServer extraction complete - {len(results)} records pulled.")

        cursor.close()
        connection.close()
        return results
    
    except Exception as e:
        logger.error(f"Object server extraction failed - {e}")
        return None            