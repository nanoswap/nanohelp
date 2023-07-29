import unittest
from unittest.mock import Mock, patch, MagicMock
from nanohelp.secret import SecretManager
from google.cloud import secretmanager


class TestSecretManager(unittest.TestCase):

    def setUp(self):
        self.manager = SecretManager()
        self.manager.secret_manager_client = Mock()
        self.project = "test_project"
        self.name = "test_name"
        self.private_key = "test_private_key"

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


    @patch.object(secretmanager.SecretManagerServiceClient, 'create_secret')
    def test_create_secret(self, mock_create_secret):
        self.manager.create_secret(self.project, self.name)
        mock_create_secret.assert_called_once()

    @patch.object(secretmanager.SecretManagerServiceClient, 'create_secret')
    @patch.object(secretmanager.SecretManagerServiceClient, 'list_secrets')
    @patch.object(secretmanager.SecretManagerServiceClient, 'add_secret_version')
    def test_store_private_key_secret_exists(self, mock_add_secret_version, mock_list_secrets, mock_create_secret):
        # Mock existing secret
        mock_secret = MagicMock()
        mock_secret.name = self.name
        mock_list_secrets.return_value = [mock_secret]

        self.manager.store_private_key(self.project, self.name, self.private_key)

        mock_create_secret.assert_not_called()
        mock_add_secret_version.assert_called_once()

    @patch.object(secretmanager.SecretManagerServiceClient, 'create_secret')
    @patch.object(secretmanager.SecretManagerServiceClient, 'list_secrets')
    @patch.object(secretmanager.SecretManagerServiceClient, 'add_secret_version')
    def test_store_private_key_secret_not_exists(self, mock_add_secret_version, mock_list_secrets, mock_create_secret):
        # Mock no existing secrets
        mock_list_secrets.return_value = []

        self.manager.store_private_key(self.project, self.name, self.private_key)

        mock_create_secret.assert_called_once()
        mock_add_secret_version.assert_called_once()

    def test_get_private_key(self):
        self.manager.secret_manager_client.secret_version_path.return_value = 'mocked_path'
        self.manager.secret_manager_client.access_secret_version.return_value.payload.data.decode.return_value = 'mocked_key'
        key = self.manager.get_private_key('mock_project', 'mock_name')
        self.assertEqual(key, 'mocked_key')
