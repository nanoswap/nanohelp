# nanohelp
Business logic to abstract the raw nano node RPC logic

## Documentation

https://nanohelp.readthedocs.io/en/latest/

## Installation

```
pip install nanohelp
```

## Usage

```python
from nanohelp.secret import SecretManager
from nanohelp.wallet import WalletManager

# Initialize a SecretManager
secret_manager = SecretManager()

# Initialize a WalletManager, passing in the secret manager
wallet_manager = WalletManager(secret_manager)

# Define user and project details
user1 = "user1"
user2 = "user2"
project_id = "my-project"

# Create a new wallet for User1, this also generates and stores a new private key
wallet_id_user1, account_address_user1 = wallet_manager.create_wallet(user1)

# Create a new wallet for User2
wallet_id_user2, account_address_user2 = wallet_manager.create_wallet(user2)

# Transaction from User1's account to User2's account
amount = 1000  # amount of Nano to be sent
transaction_block = wallet_manager.make_transaction(
    wallet_id_user1,
    account_address_user1,
    account_address_user2,
    amount, 
    secret_manager.get_private_key(project_id, user1)
)

# Print transaction block
print(f"Transaction block: {transaction_block}")
```
