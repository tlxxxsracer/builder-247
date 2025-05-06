"""Logging utility for Transaction ID Cleanup Operations."""

from typing import Optional, Union, Dict, Any
from .logging import logger, log_section, log_key_value


def log_transaction_id_cleanup_start(
    transaction_id: str,
    context: Optional[str] = None
) -> None:
    """
    Log the start of a transaction ID cleanup operation.

    Args:
        transaction_id (str): The unique transaction ID being processed
        context (Optional[str]): Optional context about the cleanup operation
    """
    log_section(f"Transaction ID Cleanup: {transaction_id}")
    if context:
        log_key_value("Context", context)


def log_transaction_id_cleanup_details(
    transaction_id: str,
    details: Union[str, Dict[str, Any]]
) -> None:
    """
    Log detailed information about a transaction ID cleanup.

    Args:
        transaction_id (str): The unique transaction ID being processed
        details (Union[str, Dict[str, Any]]): Details of the cleanup operation
    """
    logger.info(f"Cleanup Details for Transaction ID {transaction_id}:")
    if isinstance(details, dict):
        for key, value in details.items():
            log_key_value(str(key), value)
    else:
        log_key_value("Details", details)


def log_transaction_id_cleanup_success(
    transaction_id: str,
    result: Optional[Union[str, Dict[str, Any]]] = None
) -> None:
    """
    Log a successful transaction ID cleanup operation.

    Args:
        transaction_id (str): The unique transaction ID that was processed
        result (Optional[Union[str, Dict[str, Any]]]): Optional result details
    """
    logger.info(f"✓ Transaction ID {transaction_id} Cleanup Successful")
    if result:
        log_transaction_id_cleanup_details(transaction_id, result)


def log_transaction_id_cleanup_failure(
    transaction_id: str,
    error: Union[str, Exception],
    additional_context: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log a failed transaction ID cleanup operation.

    Args:
        transaction_id (str): The unique transaction ID that failed to be processed
        error (Union[str, Exception]): The error that occurred
        additional_context (Optional[Dict[str, Any]]): Optional additional context about the failure
    """
    logger.error(f"✗ Transaction ID {transaction_id} Cleanup Failed")
    error_message = str(error) if isinstance(error, Exception) else error
    log_key_value("Error", error_message)

    if additional_context:
        logger.info("Additional Context:")
        for key, value in additional_context.items():
            log_key_value(str(key), value)