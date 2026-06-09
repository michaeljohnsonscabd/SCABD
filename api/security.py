"""
SCABD API Security and Middleware
"""
import functools
import logging
import datetime
from config import settings

# In-memory storage for demo purposes. In production, use Redis or a DB.
API_KEYS = {
    "SCABD-PRO-2024": {"owner": "Default Client", "quota": 1000, "used": 0},
}

def validate_api_key(api_key):
    """Checks if the API key is valid and has remaining quota."""
    if api_key in API_KEYS:
        client_info = API_KEYS[api_key]
        if client_info["used"] < client_info["quota"]:
            client_info["used"] += 1
            return True, client_info
    return False, None

def require_api_key(func):
    """Decorator to enforce API key validation on endpoints."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Improved header extraction from both args and kwargs
        headers = kwargs.get('headers')
        if not headers and args:
            # Check if headers is passed as the first positional argument if it's not in kwargs
            # This is a heuristic for the current simplified API structure
            headers = args[0] if isinstance(args[0], dict) else {}
        else:
            headers = headers or {}

        api_key = headers.get('X-SCABD-API-KEY')

        is_valid, client_info = validate_api_key(api_key)

        # Audit Logging
        timestamp = datetime.datetime.now().isoformat()
        client_name = client_info['owner'] if client_info else "UNKNOWN"
        logging.info(f"[{timestamp}] API CALL: {func.__name__} | Client: {client_name} | Success: {is_valid}")
        print(f"[AUDIT] {timestamp} - API Access: {func.__name__} by {client_name} (Status: {is_valid})")

        if not is_valid:
            return {"error": "403 Forbidden - Invalid or Expired API Key"}, 403

        return func(*args, **kwargs)
    return wrapper
