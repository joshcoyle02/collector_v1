# Runs the extraction function with the environments details passed in.
# Information from the secure form should be placed in here.
# Paramterers are subject to change when we get access to Netcool.

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