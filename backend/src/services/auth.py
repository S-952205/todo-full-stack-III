from fastapi import HTTPException, status
from typing import Dict, Any, Optional
from jose import jwt, JWTError  # Using python-jose which provides jwt functionality


def validate_mcp_request(user_id: str, expected_user_id: str) -> bool:
    """
    Validate user access specifically for MCP tool requests.

    Args:
        user_id: The user_id provided in the MCP tool request
        expected_user_id: The expected authenticated user_id

    Returns:
        bool: True if access is granted, raises HTTPException if not
    """
    if user_id != expected_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="MCP tool access denied: User ID mismatch"
        )
    return True


def extract_user_id_from_token(token: str, secret_key: str) -> Optional[str]:
    """
    Extract user_id from JWT token for MCP server use.

    Args:
        token: JWT token string
        secret_key: Secret key used to decode the token

    Returns:
        str: user_id if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload.get("userId") or payload.get("sub") or payload.get("user_id")
        return str(user_id) if user_id else None
    except jwt.JWTError:
        return None