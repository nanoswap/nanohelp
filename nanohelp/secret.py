from typing import Self
import time
import secrets
from google.cloud import secretmanager
import logging

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SecretManager:
    """Class to handle operations related to Google Cloud Secret Manager."""

    def __init__(self: Self):
        self.secret_manager_client = secretmanager.SecretManagerServiceClient()

    def generate_private_key(self: Self) -> str:
        """Generate a private key using the /dev/urandom command.

        Returns:
            The generated key
        """
        return secrets.token_hex(32)  # 32 bytes = 64 hexadecimal characters


    def generate_and_store_private_key(
            self: Self,
            project: str,
            name: str) -> str:
        """This method generates a private key and stores it in Google Secret Manager.

        Params:
            - project: the project to store the secret in
            - name: the secret name to store the private key for

        Raises:
            - RuntimeError: If unable to store the secret.
        """
        private_key = self.generate_private_key()
        self.store_private_key(project, name, private_key)
        return private_key

    def store_private_key(
            self: Self,
            project: str,
            name: str,
            private_key: str) -> None:
        """Storing a private key based on a index in Google Secret Manager.

        Params:
            - project: the project to store the secret in
            - name: the name of the secret
            - private_key: the private key to store

        Raises:
            - RuntimeError: If unable to store the secret.
        """
        try:
            # Create a new secret version
            secret = self.secret_manager_client.secret_path(
                project,
                name,
            )

            # Add the secret version
            self.secret_manager_client.add_secret_version(
                parent=secret,
                payload=secretmanager.SecretPayload(
                    data=private_key.encode('UTF-8')
                )
            )
        except Exception as e:
            LOG.error(f"Failed to store private key for {name}: {e}")
            LOG.exception(e)
            raise RuntimeError("Unable to store secret: {}".format(e)) from e

    def get_private_key(
            self: Self,
            project: str,
            name: str,
            version: str = "latest") -> str:
        """Fetch the private key from Google Secret Manager.

        Params:
            - project: the project to fetch the secret from
            - user: the user to fetch the private key for
            - version: the version of the secret to fetch

        Returns:
            - private_key: the private key for the user

        Raises:
            - RuntimeError: If unable to retrieve the secret.
        """
        try:
            # Build the resource name of the secret version.
            name = self.secret_manager_client.secret_version_path(
                project,
                name,
                version
            )

            # Access the secret version.
            response = self.secret_manager_client.access_secret_version(name)

            # Get the payload of the secret.
            payload = response.payload.data.decode('UTF-8')

            return payload
        except Exception as e:
            LOG.error(f"Failed to retrieve private key for {name}: {e}")
            LOG.exception(e)
            raise RuntimeError("Unable to retrieve secret: {}".format(e)) from e

    def rotate_private_key(
            self: Self,
            project: str,
            name: str,
            new_key: str) -> None:
        """Rotate a private key, replacing it with a new version.

        **Caution**: the old private key will be lost, and if it is used for
        anything (ex: a crypto wallet), it will no longer work with the new key.

        This will generate a new private key and store it in Google Secret Manager,
        effectively replacing the old one.

        Params:
            - project: the project to store the secret in
            - name: the name of the secret
            - new_key: the new private key to store

        Returns:
            - The new private key that was generated.

        Raises:
            - RuntimeError: If unable to generate and store the new private key.
        """
        raise NotImplementedError("No use case found for rotating private keys (using this for crypto wallets is a bad idea)")

        try:
            # Generate and store a new private key
            return self.generate_and_store_private_key(project, name, new_key)
        except Exception as e:
            raise RuntimeError(f"Unable to rotate private key: {e}") from e
