# Runs the extraction and saves the results to a JSON file.
# The collector runs on the same host as the mock, so no bastion or tunnel is needed.

import json
import logging
from datetime import datetime
from collector.run_extraction import run_extraction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    results = run_extraction(
        key_path="/home/ubuntu/.ssh/id_rsa",
        netcool_host="172.31.42.80",
        reporter_db_port=5432,
        db_user="netcool",
        db_password="netcool_password",
        db_name="netcool_mock",
        last_extraction_date=None
    )

    if results is None:
        logger.error("Extraction failed - no output written")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"extraction_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(results, f, indent=2, default=str)
        logger.info("Results written to %s", filename)