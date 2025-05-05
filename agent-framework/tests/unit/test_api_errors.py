"""
Unit tests for API error handling utilities.

This module tests the custom error classes and error handling mechanisms
defined in prometheus_swarm.utils.api_errors.
"""

import pytest
from prometheus_swarm.utils.api_errors import (
    APIError, AuthenticationError, RateLimitError, 
    ResourceNotFoundError, InvalidRequestError, 
    NetworkError, handle_api_error
)

def test_base_api_error():
    """Test base APIError functionality."""
    error = APIError("Test message", status_code=400, response={"detail": "Error"})
    
    assert str(error) == "Test message"
    assert error.message == "Test message"
    assert error.status_code == 400
    assert error.response == {"detail": "Error"}

def test_authentication_error():
    """Test AuthenticationError specific behavior."""
    error = AuthenticationError("Invalid credentials")
    
    assert isinstance(error, APIError)
    assert str(error) == "Invalid credentials"

def test_rate_limit_error():
    """Test RateLimitError specific behavior."""
    error = RateLimitError("Rate limit exceeded", status_code=429)
    
    assert isinstance(error, APIError)
    assert error.status_code == 429
    assert str(error) == "Rate limit exceeded"

def test_resource_not_found_error():
    """Test ResourceNotFoundError specific behavior."""
    error = ResourceNotFoundError("Resource not found", status_code=404)
    
    assert isinstance(error, APIError)
    assert error.status_code == 404
    assert str(error) == "Resource not found"

def test_invalid_request_error():
    """Test InvalidRequestError specific behavior."""
    error = InvalidRequestError("Invalid request parameters")
    
    assert isinstance(error, APIError)
    assert str(error) == "Invalid request parameters"

def test_network_error():
    """Test NetworkError specific behavior."""
    error = NetworkError("Connection failed")
    
    assert isinstance(error, APIError)
    assert str(error) == "Connection failed"

def test_handle_api_error_authentication():
    """Test error handling for authentication errors."""
    with pytest.raises(AuthenticationError):
        handle_api_error(AuthenticationError("Auth failed"))

def test_handle_api_error_rate_limit():
    """Test error handling for rate limit errors."""
    with pytest.raises(RateLimitError):
        handle_api_error(RateLimitError("Rate limit"))

def test_handle_api_error_network_timeout():
    """Test error handling for timeout errors."""
    with pytest.raises(NetworkError, match="API request timed out"):
        handle_api_error(Exception("Request timed out"))

def test_handle_api_error_network_connection():
    """Test error handling for connection errors."""
    with pytest.raises(NetworkError, match="Network connection error"):
        handle_api_error(Exception("Connection refused"))

def test_handle_api_error_unexpected():
    """Test handling of unexpected errors."""
    error = handle_api_error(Exception("Unknown error"))
    
    assert isinstance(error, APIError)
    assert "Unexpected API error" in str(error)