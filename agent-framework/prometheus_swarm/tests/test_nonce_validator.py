import time
import threading
import pytest
from prometheus_swarm.utils.nonce_validator import DistributedNonceValidator

def test_nonce_validator_basic_functionality():
    """Test basic nonce validation functionality."""
    validator = DistributedNonceValidator()
    
    # First occurrence of nonce should be valid
    assert validator.validate_nonce("unique_nonce_1", "node1") == True
    
    # Same nonce from same node should be invalid
    assert validator.validate_nonce("unique_nonce_1", "node1") == False
    
    # Same nonce from different node should be valid
    assert validator.validate_nonce("unique_nonce_1", "node2") == True

def test_nonce_validator_empty_inputs():
    """Test handling of empty or None inputs."""
    validator = DistributedNonceValidator()
    
    assert validator.validate_nonce("", "node1") == False
    assert validator.validate_nonce("nonce", "") == False
    assert validator.validate_nonce("", "") == False

def test_nonce_validator_expiration():
    """Test nonce expiration mechanism."""
    validator = DistributedNonceValidator(expiration_time=1)
    
    assert validator.validate_nonce("expired_nonce", "node1") == True
    
    # Wait for expiration
    time.sleep(2)
    
    # Nonce should now be reusable
    assert validator.validate_nonce("expired_nonce", "node1") == True

def test_nonce_validator_max_nonces():
    """Test nonce limit functionality."""
    validator = DistributedNonceValidator(max_nonces=3)
    
    # Add more nonces than max allowed
    for i in range(5):
        validator.validate_nonce(f"nonce_{i}", "node1")
    
    # Check that nonces are being pruned
    assert len(validator._nonces) == 3

def test_cross_thread_duplicate_nonce_validation():
    """
    Test that multiple threads cannot validate the same nonce concurrently.
    This test ensures thread-safe unique nonce validation.
    """
    validator = DistributedNonceValidator()
    concurrent_results = []
    shared_nonce = "parallel_test_nonce"

    def attempt_nonce_validation(node_id):
        result = validator.validate_nonce(shared_nonce, node_id)
        concurrent_results.append(result)

    # Create multiple threads trying to validate the same nonce
    threads = [
        threading.Thread(target=attempt_nonce_validation, args=(f"node_{i}"))
        for i in range(10)
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Only one thread should succeed in validating the nonce
    assert concurrent_results.count(True) == 1
    assert concurrent_results.count(False) == 9