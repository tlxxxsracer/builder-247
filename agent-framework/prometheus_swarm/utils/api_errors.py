"""
Custom error handling module for API interactions.

This module defines custom exceptions and error handling mechanisms
for managing API-related errors across different client implementations.
"""

class APIError(Exception):
    """Base class for API-related errors."""
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response

class AuthenticationError(APIError):
    """Raised when authentication with an API fails."""
    pass

class RateLimitError(APIError):
    """Raised when API rate limits are exceeded."""
    pass

class ResourceNotFoundError(APIError):
    """Raised when a requested resource is not found."""
    pass

class InvalidRequestError(APIError):
    """Raised when the request is malformed or invalid."""
    pass

class NetworkError(APIError):
    """Raised for network-related issues during API calls."""
    pass

def handle_api_error(error):
    """
    Generic error handler for API interactions.
    
    Args:
        error (Exception): The caught exception to handle.
    
    Returns or Raises:
        APIError: Converted and more specific API error
    """
    if isinstance(error, AuthenticationError):
        return error
    elif isinstance(error, RateLimitError):
        return error
    elif isinstance(error, ResourceNotFoundError):
        return error
    elif isinstance(error, NetworkError):
        return error
    elif isinstance(error, Exception):
        error_str = str(error).lower()
        if "timeout" in error_str:
            return NetworkError("API request timed out")
        elif "connection" in error_str:
            return NetworkError("Network connection error")
    
    return APIError(f"Unexpected API error: {str(error)}")