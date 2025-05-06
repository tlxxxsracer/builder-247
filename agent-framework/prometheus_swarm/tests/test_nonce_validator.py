import time
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
    assert len(validator._nonces) <= 3

def test_nonce_validator_thread_safety(num_threads=10, nonces_per_thread=100):
    """Test thread-safe behavior of nonce validator."""
    from concurrent.futures import ThreadPoolExecutor
    
    validator = DistributedNonceValidator()
    valid_nonces = 0
    invalid_nonces = 0
    
    def test_thread(thread_id):
        nonlocal valid_nonces, invalid_nonces
        for i in range(nonces_per_thread):
            nonce = f"thread_{thread_id}_nonce_{i}"
            is_valid = validator.validate_nonce(nonce, f"node_{thread_id}")
            if is_valid:
                valid_nonces += 1
            else:
                invalid_nonces += 1
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(test_thread, range(num_threads))
    
    # Expect the number of valid nonces to equal total nonces
    assert valid_nonces == num_threads * nonces_per_thread
    assert invalid_nonces > 0