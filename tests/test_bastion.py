# This file tests the connecttobastion() function in isolation without needing a real server or SSH key.This file tests the connect_to_bastion() 
# function in isolation without needing a real server or SSH key. It uses mocking to simulate two scenarios — a successful connection where the 
# function should return an active client session, and a failed connection where the function should return None. 

# Results of each test are logged with a timestamp to test_bastion.txt.

#TO RUN - python -m unittest tests/test_bastion.py

import unittest
import logging
from unittest.mock import patch, MagicMock
from collector.bastion import connect_to_bastion

# Set up logging to a .txt file
log_handler = logging.FileHandler('tests/test_logs/test_bastion.txt')
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger('test_bastion')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

class TestBastion(unittest.TestCase):

    @patch('collector.bastion.paramiko.RSAKey.from_private_key_file')
    @patch('collector.bastion.paramiko.SSHClient')
    def test_successful_connection(self, mock_ssh_client, mock_rsa_key):
        mock_client = MagicMock()
        mock_ssh_client.return_value = mock_client
        result = connect_to_bastion('192.168.1.1', 'testuser', '/fake/key/path')
        self.assertIsNotNone(result)
        logger.info("test_successful_connection - PASSED")

    @patch('collector.bastion.paramiko.RSAKey.from_private_key_file')
    @patch('collector.bastion.paramiko.SSHClient')
    def test_failed_connection(self, mock_ssh_client, mock_rsa_key):
        mock_ssh_client.return_value.connect.side_effect = Exception("Connection refused")
        result = connect_to_bastion('192.168.1.1', 'testuser', '/fake/key/path')
        self.assertIsNone(result)
        logger.info("test_failed_connection - PASSED")

if __name__ == '__main__':
    unittest.main()