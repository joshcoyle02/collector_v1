# This file tests the connect_to_reporter_db() function in isolation without needing a real database connection.
# It uses mocking to simulate three scenarios — a successful first run where all records are pulled,
# a successful subsequent run where only records since the last extraction date are pulled,
# and a failed connection where the function should return None.

# Results of each test are logged with a timestamp to test_reporter_db.txt.

#TO RUN - python -m unittest tests/test_reporter_db.py

import unittest
import logging
from unittest.mock import patch, MagicMock
from collector.reporter_db import connect_to_reporter_db

# Clear any existing logging handlers
logging.root.handlers = []

# Set up logging to a .txt file
log_handler = logging.FileHandler('tests/test_logs/test_reporter_db.txt')
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger('test_reporter_db')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

class TestReporterDB(unittest.TestCase):

    @patch('collector.reporter_db.jaydebeapi.connect')
    def test_successful_first_run(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('event1',), ('event2',)]
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = connect_to_reporter_db(None, 'jdbc_url', 'user', 'password', 'jar_path', last_extraction_date=None)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        logger.info("test_successful_first_run - PASSED")

    @patch('collector.reporter_db.jaydebeapi.connect')
    def test_successful_subsequent_run(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('event1',)]
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = connect_to_reporter_db(None, 'jdbc_url', 'user', 'password', 'jar_path', last_extraction_date='2026-01-01')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        logger.info("test_successful_subsequent_run - PASSED")

    @patch('collector.reporter_db.jaydebeapi.connect')
    def test_failed_connection(self, mock_connect):
        mock_connect.side_effect = Exception("Connection refused")

        result = connect_to_reporter_db(None, 'jdbc_url', 'user', 'password', 'jar_path')
        self.assertIsNone(result)
        logger.info("test_failed_connection - PASSED")

if __name__ == '__main__':
    unittest.main()