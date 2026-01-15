from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from sqlmodel import Session
from db import get_session
from models import User, UserCreate, UserResponse, TokenResponse
from auth import verify_jwt_token
from jose import jwt
from config import settings
import uuid
from datetime import datetime, timedelta
from passlib.context import CryptContext
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)

@router.post("/auth/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(
    user_data: UserCreate,
    session: Session = Depends(get_session)
) -> UserResponse:
    """
    Create a new user account.
    """
    try:
        # Check if user already exists
        existing_user = session.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            name=user_data.name,
            password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        logger.info(f"User created successfully: {user.id}")

        # Return user response without password
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.post("/auth/login", response_model=TokenResponse)
def login(
    credentials: Dict[str, str],
    session: Session = Depends(get_session)
) -> TokenResponse:
    """
    Authenticate user and return JWT token.
    """
    email = credentials.get("email")
    password = credentials.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    try:
        # Find user by email
        user = session.query(User).filter(User.email == email).first()

        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Generate JWT token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

        # Prepare token payload
        token_data = {
            "sub": user.id,
            "userId": user.id,
            "email": user.email,
            "name": user.name,
            "exp": datetime.utcnow() + access_token_expires
        }

        access_token = jwt.encode(token_data, settings.better_auth_secret, algorithm="HS256")

        logger.info(f"User logged in successfully: {user.id}")

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to login"
        )


@router.post("/auth/logout")
def logout():
    """
    Logout user (client-side cleanup only).
    """
    return {"message": "Successfully logged out"}


@router.post("/auth/refresh")
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    Refresh the JWT token.
    """
    try:
        # Verify the current token
        payload = verify_jwt_token(credentials)

        # Generate a new token with extended expiry
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

        # Prepare new token payload
        new_token_data = {
            "sub": payload.get("sub"),
            "userId": payload.get("userId"),
            "email": payload.get("email"),
            "name": payload.get("name"),
            "exp": datetime.utcnow() + access_token_expires
        }

        new_access_token = jwt.encode(new_token_data, settings.better_auth_secret, algorithm="HS256")

        return {"access_token": new_access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )