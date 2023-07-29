from basicnanoclient.nano import BasicNanoClient
from typing import List, Tuple, Optional, Self
import logging

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class WalletManager:
    """Business logic to abstract the raw nano node RPC logic.

    This class is responsible for creating wallets, adding accounts to wallets,
    and making transactions.
    """
    def __init__(
            self: Self,
            node_address: str = "http://127.0.0.1:17076") -> None:
        """Initialize the wallet manager.

        Params:
            - node_address: the address of the node to connect to.
                Defaults to the local node at port 17076.
        """
        self.client = BasicNanoClient(node_address)

    def create_wallet(self: Self) -> Optional[Tuple[str, str, str]]:
        """Create a new wallet.

        Returns: a tuple containing wallet_id, account_address and private_key
        """
        try:
            private_key = self.client.generate_private_key()
            wallet_id = self.client.wallet_create(private_key)['wallet']
            account_address = self.client.accounts_create(wallet_id)['accounts'][0]
        except Exception as e:
            LOG.error(f"Failed to create wallet: {e}")
            LOG.exception(e)
            return None

        return wallet_id, account_address, private_key

    def add_account_to_wallet(self: Self, wallet_id: str) -> Optional[str]:
        """Add a new account to an existing wallet.

        Params:
            - wallet_id: the wallet id to add the account to
        """
        try:
            account_address = self.client.accounts_create(wallet_id)['accounts'][0]
        except Exception as e:
            LOG.error(f"Failed to add account to wallet {wallet_id}: {e}")
            LOG.exception(e)
            return None

        return account_address

    def make_transaction(
            self: Self,
            source_wallet: str,
            source_account: str,
            destination_account: str,
            amount: int,
            private_key: str,
            retries: int = 3) -> Optional[str]:
        """Make a transaction.

        Params:
            - source_wallet: the wallet id of the source account
            - source_account: the address of the source account
            - destination_account: the address of the destination account
            - amount: the amount of Nano to be sent
            - private_key: the private key of the source account
            - retries: the number of times to retry the transaction in case of failure  # noqa: E501

        Returns: the transaction block
        """
        if retries <= 0:
            raise ValueError("Transaction failed after multiple retries")

        try:
            account_list = self.client.account_list(source_wallet)['accounts']
            if source_account not in account_list:
                raise ValueError(f"Account {source_account} doesn't belong to wallet {source_wallet}")  # noqa: E501

            # Check if the account has enough balance
            balance = self.client.account_info(source_account)['balance']
            if int(balance) < amount:
                raise ValueError(f"Account {source_account} has insufficient balance")  # noqa: E501

            # Make the transaction
            transaction = self.client.send(
                source_wallet,
                source_account,
                destination_account,
                amount,
                private_key
            )
            LOG.info(f"Transaction successful: {transaction}")
            block = transaction.get('block')
            LOG.info(f"Block: {block}")
            return block

        except Exception as e:
            LOG.error(f"Transaction failed: {e}")
            LOG.exception(e)
            # TODO: redo retry to use decorator
            return self.make_transaction(
                source_wallet,
                source_account,
                destination_account,
                amount,
                private_key,
                retries - 1
            )
