from .db import session
from datetime import datetime,timedelta
from .models import Otp, User
from app.utils.logger import get_logger

from typing import Optional, Callable
import os 
import json
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
import random
import bcrypt
from functools import wraps
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

security = HTTPBearer()

logger = get_logger(__name__)
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 7 days


def generate_otp(email: str):
    if not email:
        return None

    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))

    # Set expiry time (use UTC for consistency)
    expiry_time = datetime.now() + timedelta(minutes=10)

    # Create OTP object
    otp_obj = Otp(
        email=email,
        otp=otp,
        expires_at=expiry_time
    )

    try:
        # Add and commit to DB
        session.add(otp_obj)
        session.commit()
        session.refresh(otp_obj)
        return otp_obj
    except Exception as e:
        session.rollback()
        raise e  

    
def verify_user(email,otp):
    if not email or not otp:
        return None
    
    try:
        result = session.query(Otp).filter(Otp.email == email, Otp.otp == otp).first()
        if not result:
            return False
        return True
    except Exception as e:
        session.rollback()
        raise e  
        
def create_user(user_data):
    """
    Create a new user in the database
    """
    try:
        # Normalize email to lowercase if it exists
        if 'email' in user_data and user_data['email']:
            user_data['email'] = user_data['email'].lower()
            
        if find_user(user_data['email']) or  find_user(user_data['username']):
            return None
        
        pw_hashed = hash_password(user_data.pop('password'))
        user_data['hashed_password'] = pw_hashed
        print(user_data)
        new_user = User(**user_data)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise
     
        
def find_user(identifier):
    try:
        if "@" in identifier:
            user = session.query(User).filter(User.email == identifier).first()
        else:
            user = session.query(User).filter(User.username == identifier).first()
        return user
    
    except Exception as e:
        session.rollback()
        logger.error(f"Error finding user: {str(e)}")
        raise

def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt and return a UTF-8 string.
    """
    try:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        return hashed_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f"Error hashing password: {str(e)}")
        raise


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Compare a plaintext password with a hashed one (returns True or False).
    """
    try:
        # bcrypt.checkpw expects both arguments as bytes
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        logger.error(f"Error in password matching: {str(e)}")
        raise


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new JWT token
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time
        
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token
        
    Returns:
        Tuple of (payload, error_dict) where one will be None
    """
    try:
        if not token or not isinstance(token, str):
            return None, {"error": "token_invalid", "message": "Invalid token format"}
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
                
        return payload
        
    except ExpiredSignatureError:
        logger.warning(f"Token expired: {token[:10]}...")
        return {"error": "token_expired", "message": "Your session has expired. Please log in again."}
    except JWTError as e:
        logger.warning(f"Invalid token: {token[:10]}... - {str(e)}")
        return {"error": "token_invalid", "message": "Invalid authentication token. Please log in again."}
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return {"error": "token_error", "message": "Authentication error. Please log in again."}

def get_current_user(token: str):
    """
    Get user from database based on token
    
    Args:
        token: JWT token
        
    Returns:
        User object or None if token is invalid
    """
    try:
        payload, error = verify_token(token)
        print(payload)
        if error or not payload:
            return None
        
        # Handle both 'sub' (email) and 'user_id' fields for backward compatibility
        user_identifier = payload.get('sub') or payload.get('user_id')
        if not user_identifier:
            logger.warning("Token payload missing user identifier")
            return None
        
        # Try to find user by email first (if it contains @), then by ID
        if '@' in str(user_identifier):
            return find_user(email=user_identifier)
        elif user_identifier.isdigit():
            return find_user(phone=user_identifier)
        else:
            try:
                user_id = int(user_identifier)
                return find_user(id=user_id)
            except (ValueError, TypeError):
                return find_user(email=user_identifier)
            
                
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        return None

def get_optional_user_from_event(event):
    """
    Extract user information from event if authentication token is present (optional auth)
    
    Args:
        event: Lambda event object
        
    Returns:
        User payload dict or None if not authenticated
    """
    try:
        # Extract token from Authorization header
        headers = event.get('headers', {})
        auth_header = headers.get('authorization') or headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        if not token:
            return None
        
        # Verify token
        payload, error = verify_token(token)
        
        if error or not payload:
            logger.warning(f"Optional auth failed: {error}")
            return None
            
        return payload
        
    except Exception as e:
        logger.warning(f"Error in optional user extraction: {str(e)}")
        return None

def require_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload or payload.get("error") :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=payload.get("message") if payload else "Invalid token"
        )
    return payload  # will be available in route




def validate_jwt_secret():
    """
    Validate that JWT secret is properly configured
    
    Returns:
        Boolean indicating if JWT is properly configured
    """
    if not SECRET_KEY:
        logger.error("JWT_SECRET_KEY environment variable not set")
        return False
    
    if len(SECRET_KEY) < 32:
        logger.warning("JWT_SECRET_KEY is shorter than recommended (32 characters)")
        return False
    
    return True

# Validate configuration on module load
if not validate_jwt_secret():
    logger.error("JWT configuration is invalid. Authentication will not work properly.")