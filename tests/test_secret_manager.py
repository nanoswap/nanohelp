import unittest
from unittest.mock import Mock, patch
from nanohelp.secret import SecretManager

class TestSecretManager(unittest.TestCase):

    def setUp(self):
        self.manager = SecretManager()
        self.manager.secret_manager_client = Mock()

    def test_generate_private_key(self):
        key = self.manager.generate_private_key()
        self.assertEqual(len(key), 64)

    @patch('nanohelp.secret.secrets.token_hex')
    def test_generate_and_store_private_key(self, mock_token_hex):
        mock_token_hex.return_value = 'mocked_key'
        self.manager.store_private_key = Mock()
        key = self.manager.generate_and_store_private_key('mock_project', 'mock_user')
        self.assertEqual(key, 'mocked_key')
        self.manager.store_private_key.assert_called_once_with('mock_project', 'mock_user', 'mocked_key')

    @patch('nanohelp.secret.time.time', return_value=100)
    def test_store_private_key(self, mock_time):
        self.manager.secret_manager_client.secret_version_path.return_value = 'mocked_path'
        self.manager.store_private_key('mock_project', 'mock_name', 'mock_key')
        self.manager.secret_manager_client.add_secret_version.assert_called_once()

    def test_get_private_key(self):
        self.manager.secret_manager_client.secret_version_path.return_value = 'mocked_path'
        self.manager.secret_manager_client.access_secret_version.return_value.payload.data.decode.return_value = 'mocked_key'
        key = self.manager.get_private_key('mock_project', 'mock_name')
        self.assertEqual(key, 'mocked_key')
