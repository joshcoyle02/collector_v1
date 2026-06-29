# This file tests the connect_to_impact() function in isolation without needing a real server.
# It uses mocking to simulate three scenarios — a successful first run where all policy files are pulled,
# a successful subsequent run where only files modified since the last extraction date are pulled,
# and a failed connection where the function should return None.

# Results of each test are logged with a timestamp to test_impact.txt.

# TO RUN - python -m unittest tests/test_object_server.py

import unittest
import logging
from unittest.mock import patch, MagicMock
from collector.impact import connect_to_impact

# Clear any existing logging handlers
logging.root.handlers = []

# Set up logging to a .txt file
log_handler = logging.FileHandler('tests/test_logs/test_impact.txt')
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger('test_impact')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

class TestImpact(unittest.TestCase):

    def test_successful_first_run(self):
        mock_client = MagicMock()
        mock_sftp = MagicMock()
        mock_client.open_sftp.return_value = mock_sftp
        mock_sftp.listdir.return_value = ['policy1.xml', 'policy2.xml']

        result = connect_to_impact(mock_client, last_extraction_date=None)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        logger.info("test_successful_first_run - PASSED")

    def test_successful_subsequent_run(self):
        mock_client = MagicMock()
        mock_sftp = MagicMock()
        mock_client.open_sftp.return_value = mock_sftp
        mock_sftp.listdir.return_value = ['policy1.xml']
        mock_sftp.stat.return_value.st_mtime = 9999999999

        result = connect_to_impact(mock_client, last_extraction_date=1000000000)
        self.assertIsNotNone(result)
        logger.info("test_successful_subsequent_run - PASSED")

    def test_failed_connection(self):
        mock_client = MagicMock()
        mock_client.open_sftp.side_effect = Exception("SFTP connection failed")

        result = connect_to_impact(mock_client, last_extraction_date=None)
        self.assertIsNone(result)
        logger.info("test_failed_connection - PASSED")

if __name__ == '__main__':
    unittest.main()