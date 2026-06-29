## The run extraction script:
1. Calls the Bastion connection
2. Creates a tunnel to each target.
3. Calls each target function in order.
4. Collects the results.
5. Stores everything to S3.
6. Closes all tunnels
7. Closes the bastion session
8. Logs a summary of what succeeded and what failed.

# ===================================================================#

hostname              →  Bastion IP address
username              →  SSH username
key_path              →  path to private key
jdbc_url              →  Reporter DB connection string
db_user               →  database username
db_password           →  database password
jar_path              →  path to JDBC driver file
last_extraction_date  →  None on first run, date on subsequent runs