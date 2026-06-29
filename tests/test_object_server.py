# This file tests the connect_to_object_server() function in isolation without needing a real database connection.
# It uses mocking to simulate three scenarios — a successful first run where all alerts and rules are pulled,
# a successful subsequent run where only records since the last extraction date are pulled,
# and a failed connection where the function should return None.

# Results of each test are logged with a timestamp to test_object_server.txt.

# TO RUN - python -m unittest tests/test_object_server.py

import unittest
import logging
from unittest.mock import patch, MagicMock
from collector.object_server import connect_to_object_server

# Clear any existing logging handlers
logging.root.handlers = []

# Set up logging to a .txt file
log_handler = logging.FileHandler('tests/test_logs/test_object_server.txt')
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger('test_object_server')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

class TestObjectServer(unittest.TestCase):

    @patch('collector.object_server.pymysql.connect')
    def test_successful_first_run(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('alert1',), ('alert2',)]
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = connect_to_object_server(None, 'user', 'password', last_extraction_date=None)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        logger.info("test_successful_first_run - PASSED")

    @patch('collector.object_server.pymysql.connect')
    def test_successful_subsequent_run(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('alert1',)]
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = connect_to_object_server(None, 'user', 'password', last_extraction_date='2026-01-01')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        logger.info("test_successful_subsequent_run - PASSED")

    @patch('collector.object_server.pymysql.connect')
    def test_failed_connection(self, mock_connect):
        mock_connect.side_effect = Exception("Connection refused")

        result = connect_to_object_server(None, 'user', 'password')
        self.assertIsNone(result)
        logger.info("test_failed_connection - PASSED")

if __name__ == '__main__':
    unittest.main()