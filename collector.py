## MAIN

from collector.run_extraction import run_extraction

if __name__ == "__main__":
    run_extraction(
        hostname="",        # Bastion IP address
        username="",        # SSH username
        key_path="",        # Path to private key
        jdbc_url="",        # Reporter DB connection string
        db_user="",         # Database username
        db_password="",     # Database password
        jar_path=""         # Path to JDBC driver file.
    )