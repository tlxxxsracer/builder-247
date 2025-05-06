"""Unit tests for transaction ID logging utility."""

import pytest
import logging
import re
from io import StringIO
from prometheus_swarm.utils.transaction_id_logging import (
    log_transaction_id_cleanup_start,
    log_transaction_id_cleanup_details,
    log_transaction_id_cleanup_success,
    log_transaction_id_cleanup_failure
)
from prometheus_swarm.utils.logging import logger


@pytest.fixture
def log_capture():
    """Capture log output for testing."""
    log_output = StringIO()
    handler = logging.StreamHandler(log_output)
    logger.addHandler(handler)
    
    try:
        yield log_output
    finally:
        logger.removeHandler(handler)
        log_output.close()


def test_log_transaction_id_cleanup_start(log_capture):
    """Test logging the start of a cleanup operation."""
    transaction_id = "test_txn_123"
    log_transaction_id_cleanup_start(transaction_id, "Test Context")

    log_contents = log_capture.getvalue()
    
    # Check for section header with transaction ID
    header_pattern = re.compile(r'TRANSACTION ID CLEANUP: ' + transaction_id.upper(), re.MULTILINE)
    assert header_pattern.search(log_contents) is not None, "Transaction ID cleanup header not found"
    
    # Check for context details
    assert "Context: Test Context" in log_contents, "Context details not found"


def test_log_transaction_id_cleanup_details(log_capture):
    """Test logging details of a cleanup operation."""
    transaction_id = "test_txn_456"
    details = {"status": "processing", "timestamp": "2023-01-01"}
    log_transaction_id_cleanup_details(transaction_id, details)

    log_contents = log_capture.getvalue()
    assert f"Cleanup Details for Transaction ID {transaction_id}" in log_contents
    assert "status: processing" in log_contents
    assert "timestamp: 2023-01-01" in log_contents


def test_log_transaction_id_cleanup_success(log_capture):
    """Test logging a successful cleanup operation."""
    transaction_id = "test_txn_789"
    result = {"cleaned": True, "items_removed": 5}
    log_transaction_id_cleanup_success(transaction_id, result)

    log_contents = log_capture.getvalue()
    assert f"Transaction ID {transaction_id} Cleanup Successful" in log_contents
    assert "cleaned: True" in log_contents
    assert "items_removed: 5" in log_contents


def test_log_transaction_id_cleanup_failure(log_capture):
    """Test logging a failed cleanup operation."""
    transaction_id = "test_txn_fail"
    error = "Database connection timeout"
    context = {"attempt": 1, "retry_at": "2023-01-02"}
    log_transaction_id_cleanup_failure(transaction_id, error, context)

    log_contents = log_capture.getvalue()
    assert f"Transaction ID {transaction_id} Cleanup Failed" in log_contents
    assert "Error: Database connection timeout" in log_contents
    assert "attempt: 1" in log_contents
    assert "retry_at: 2023-01-02" in log_contents


def test_log_transaction_id_cleanup_exception(log_capture):
    """Test logging a cleanup failure with an exception."""
    transaction_id = "test_txn_exception"
    error = ValueError("Invalid transaction ID")
    log_transaction_id_cleanup_failure(transaction_id, error)

    log_contents = log_capture.getvalue()
    assert f"Transaction ID {transaction_id} Cleanup Failed" in log_contents
    assert "Error: Invalid transaction ID" in log_contents