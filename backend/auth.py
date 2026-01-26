from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Dict, Any
from config import settings
import os


security = HTTPBearer()


def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Verify JWT token from Authorization header and return decoded payload.
    """
    token = credentials.credentials

    if not settings.better_auth_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: Missing BETTER_AUTH_SECRET"
        )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Extract user_id from JWT token.
    """
    payload = verify_jwt_token(credentials)

    # Extract user_id from the JWT payload
    # Assuming Better Auth JWT structure has user info
    user_id = payload.get("userId") or payload.get("sub") or payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: missing user_id",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return str(user_id)


def validate_user_access(requested_user_id: str, authenticated_user_id: str) -> bool:
    """
    Validate that the authenticated user has access to resources belonging to the requested user.

    Args:
        requested_user_id: The user_id associated with the resource being accessed
        authenticated_user_id: The user_id of the currently authenticated user

    Returns:
        bool: True if access is granted, raises HTTPException if not
    """
    if requested_user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )
    return True


def verify_resource_ownership(resource: Dict[str, Any], authenticated_user_id: str) -> bool:
    """
    Verify that a resource belongs to the authenticated user.

    Args:
        resource: Dictionary containing the resource data (must have 'user_id' key)
        authenticated_user_id: The user_id of the currently authenticated user

    Returns:
        bool: True if the resource belongs to the authenticated user, raises HTTPException if not
    """
    resource_user_id = resource.get('user_id') or resource.get('owner_id')

    if not resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Resource does not contain user identification"
        )

    if str(resource_user_id) != str(authenticated_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Resource does not belong to authenticated user"
        )

    return True