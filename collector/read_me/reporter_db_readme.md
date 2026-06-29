## Connects to the reporter DB

def connect_to_reporter_db(...)       
→  defines the function, takes in:
     client               →  the active Bastion SSH session
     jdbc_url             →  the Reporter DB connection string
     db_user              →  database username
     db_password          →  database password
     jar_path             →  path to the JDBC driver file (needed by JayDeBeApi)
     last_extraction_date →  None on first run, date on subsequent runs

## ================================================================================ ##

jaydebeapi.connect()        
→  opens the JDBC connection to Reporter DB
     "com.ibm.db2.jcc.DB2Driver"  →  the JDBC driver for IBM DB2
                                      Reporter DB runs on DB2    // Subject  to change upon implementation on netcool.
     jdbc_url                      →  where the database lives
     [db_user, db_password]        →  credentials
     jar_path                      →  the DB2 JDBC driver file

cursor = connection.cursor()
→  creates a cursor — think of it as a tool
   for executing SQL queries against the database
   like a pen you use to write queries with

logger.info(...)
→  logs successful connection