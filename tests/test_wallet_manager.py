import unittest
from unittest.mock import Mock
from nanohelp.wallet import WalletManager


class TestWalletManager(unittest.TestCase):

    def setUp(self):
        self.secret_manager = Mock()
        self.client = Mock()
        self.wallet_manager = WalletManager(self.secret_manager, 'mock_address')
        self.wallet_manager.client = self.client

    def test_create_wallet(self):
        self.secret_manager.generate_and_store_private_key.return_value = 'mock_key'
        self.client.wallet_create.return_value = {'wallet': 'mock_wallet'}
        self.client.accounts_create.return_value = {'accounts': ['mock_account']}
        result = self.wallet_manager.create_wallet('mock_name')
        self.assertEqual(result, ('mock_wallet', 'mock_account'))

    def test_add_account_to_wallet(self):
        self.client.accounts_create.return_value = {'accounts': ['mock_account']}
        result = self.wallet_manager.add_account_to_wallet('mock_wallet')
        self.assertEqual(result, 'mock_account')

    def test_make_transaction(self):
        self.client.account_list.return_value = {'accounts': ['mock_account']}
        self.client.account_info.return_value = {'balance': '1000'}
        self.client.send.return_value = {'block': 'mock_block'}
        result = self.wallet_manager.make_transaction('mock_wallet', 'mock_account', 'mock_dest_account', 100, 'mock_key')
        self.assertEqual(result, 'mock_block')
