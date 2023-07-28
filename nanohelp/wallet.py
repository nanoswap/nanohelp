from basicnanoclient.nano import BasicNanoClient
import time

class WalletManager:
    def __init__(self, node_address):
        self.client = BasicNanoClient(node_address)
        self.transaction_history = {}

    def create_wallet(self):
        """
        This method abstracts the process of creating a new wallet.

        Returns: a tuple containing wallet_id, account_address and private_key
        """
        try:
            private_key = self.client.generate_private_key()
            wallet_id = self.client.wallet_create(private_key)['wallet']
            account_address = self.client.accounts_create(wallet_id)['accounts'][0]
        except Exception as e:
            print(f"Failed to create wallet: {e}")
            return None

        return wallet_id, account_address, private_key

    def add_account_to_wallet(self, wallet_id):
        """
        Add a new account to an existing wallet.
        """
        try:
            account_address = self.client.accounts_create(wallet_id)['accounts'][0]
        except Exception as e:
            print(f"Failed to add account to wallet {wallet_id}: {e}")
            return None

        return account_address

    def make_transaction(self, source_wallet, source_account, destination_account, amount, private_key, retries=3):
        """
        This method abstracts the process of making a transaction.

        Params:
            - source_wallet: the wallet id of the source account
            - source_account: the address of the source account
            - destination_account: the address of the destination account
            - amount: the amount of Nano to be sent
            - private_key: the private key of the source account
            - retries: the number of times to retry the transaction in case of failure

        Returns: the transaction block
        """
        if retries <= 0:
            raise ValueError("Transaction failed after multiple retries")

        try:
            account_list = self.client.account_list(source_wallet)['accounts']
            if source_account not in account_list:
                raise ValueError(f"Account {source_account} doesn't belong to wallet {source_wallet}")

            # Check if the account has enough balance
            balance = self.client.account_info(source_account)['balance']
            if int(balance) < amount:
                raise ValueError(f"Account {source_account} has insufficient balance")

            # Make the transaction
            transaction = self.client.send(source_wallet, source_account, destination_account, amount, private_key)
            block = transaction.get('block')

            # Update transaction history
            if source_account not in self.transaction_history:
                self.transaction_history[source_account] = []
            self.transaction_history[source_account].append((destination_account, amount, block))

            return block

        except Exception as e:
            print(f"Transaction failed: {e}")
            # TODO: redo retry to use decorator
            return self.make_transaction(source_wallet, source_account, destination_account, amount, private_key, retries-1)

    def get_transaction_history(self, account):
        """
        Returns a list of transactions made by the account
        """
        if account not in self.transaction_history:
            return []

        return self.transaction_history[account]
