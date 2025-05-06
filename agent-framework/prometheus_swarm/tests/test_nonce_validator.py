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
    assert len(validator._nonces) == 3

def test_nonce_validator_cross_thread_duplicates(num_threads=10, shared_nonces=10):
    """Test nonce validation across different threads with shared nonces."""
    from concurrent.futures import ThreadPoolExecutor
    
    validator = DistributedNonceValidator()
    duplicate_nonces = 0
    
    def test_thread(thread_id):
        nonlocal duplicate_nonces
        valid_nonces = 0
        
        for i in range(shared_nonces):
            # Attempt to validate a shared nonce
            shared_nonce = f"shared_nonce_{i}"
            is_valid = validator.validate_nonce(shared_nonce, f"node_{thread_id}")
            
            if is_valid:
                valid_nonces += 1
            else:
                duplicate_nonces += 1
        
        return valid_nonces
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(test_thread, range(num_threads)))
    
    # At least one thread should experience a duplicate
    assert duplicate_nonces > 0
    
    # Total valid nonces should be less than total threads * shared nonces
    assert sum(results) < num_threads * shared_nonces