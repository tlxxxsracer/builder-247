import time
import hashlib
import threading
from typing import Dict, Set

class DistributedNonceValidator:
    """
    A thread-safe distributed nonce validation service that prevents replay attacks
    and ensures unique transaction processing across multiple nodes.
    """

    def __init__(self, expiration_time: int = 3600, max_nonces: int = 10000):
        """
        Initialize the Distributed Nonce Validator.

        Args:
            expiration_time (int): Number of seconds after which a nonce expires. Default is 1 hour.
            max_nonces (int): Maximum number of nonces to store before pruning. Default is 10,000.
        """
        self._nonces: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._expiration_time = expiration_time
        self._max_nonces = max_nonces

    def validate_nonce(self, nonce: str, node_id: str) -> bool:
        """
        Validate and register a unique nonce for a specific node.

        Args:
            nonce (str): The unique nonce to validate.
            node_id (str): The identifier of the node generating the nonce.

        Returns:
            bool: True if the nonce is valid and unique, False otherwise.
        """
        if not nonce or not node_id:
            return False

        # Create a unique key combining nonce and node_id
        key = self._generate_key(nonce, node_id)
        current_time = time.time()

        with self._lock:
            # Prune expired nonces if needed
            self._prune_expired_nonces(current_time)

            # Check if nonce already exists
            if key in self._nonces:
                return False

            # Add new nonce with current timestamp
            if len(self._nonces) >= self._max_nonces:
                self._remove_oldest_nonce()

            self._nonces[key] = current_time
            return True

    def _generate_key(self, nonce: str, node_id: str) -> str:
        """
        Generate a unique hash key for the nonce and node_id.

        Args:
            nonce (str): The nonce string.
            node_id (str): The node identifier.

        Returns:
            str: A unique hash key.
        """
        return hashlib.sha256(f"{nonce}:{node_id}".encode()).hexdigest()

    def _prune_expired_nonces(self, current_time: float) -> None:
        """
        Remove nonces that have expired.

        Args:
            current_time (float): The current timestamp.
        """
        # Remove expired nonces
        self._nonces = {
            key: timestamp for key, timestamp in self._nonces.items() 
            if current_time - timestamp <= self._expiration_time
        }

    def _remove_oldest_nonce(self) -> None:
        """
        Remove the oldest nonce when the maximum number of nonces is reached.
        """
        if self._nonces:
            oldest_key = min(self._nonces, key=self._nonces.get)
            del self._nonces[oldest_key]