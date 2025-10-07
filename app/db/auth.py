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

def hash_password(password):
    try:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        return hashed_password

    except Exception as e:
        session.rollback()
        logger.error(f"Error finding user: {str(e)}")
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

def require_auth(handler_function):
    """
    Decorator to require authentication for Lambda handlers
    """
    @wraps(handler_function)
    def wrapper(event, context):
        try:
            # Extract token from Authorization header
            headers = event.get('headers', {})
            auth_header = headers.get('authorization') or headers.get('Authorization')
            
            if not auth_header:
                return {
                    'statusCode': 401,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'message': 'Missing authentication token',
                        'error_type': 'missing_token'
                    })
                }
            
            if not auth_header.startswith('Bearer '):
                return {
                    'statusCode': 401,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'message': 'Invalid authentication header format',
                        'error_type': 'invalid_header'
                    })
                }
            
            token = auth_header.split(' ')[1]
            if not token:
                return {
                    'statusCode': 401,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'message': 'Missing authentication token',
                        'error_type': 'missing_token'
                    })
                }
            
            # Verify token
            payload, error = verify_token(token)
            
            if error or not payload:
                return {
                    'statusCode': 401,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'message': error.get('message', 'Authentication failed') if error else 'Invalid token',
                        'error_type': error.get('error', 'token_invalid') if error else 'token_invalid'
                    })
                }
            
            # Add user info to event for the handler
            event['user'] = payload
            return handler_function(event, context)
            
        except Exception as e:
            logger.error(f"Authentication error in require_auth: {str(e)}")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Internal authentication error',
                    'error_type': 'auth_error'
                })
            }
    
    return wrapper

def require_role(allowed_roles):
    """
    Decorator to require specific user role(s) for Lambda handlers.
    Must be used with the require_auth decorator.
    
    Args:
        allowed_roles: String or list of strings representing allowed roles
        
    Returns:
        Decorator function that checks if the user has the required role
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]
        
    def decorator(handler_function):
        @wraps(handler_function)
        def wrapper(event, context):
            try:
                # Ensure user is authenticated (require_auth should have run first)
                if 'user' not in event or event['user'] is None:
                    logger.warning("require_role called without proper authentication")
                    return {
                        'statusCode': 401,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            'message': 'Authentication required',
                            'error_type': 'not_authenticated'
                        })
                    }
                
                user_payload = event['user']
                if not isinstance(user_payload, dict):
                    logger.error(f"Invalid user payload type: {type(user_payload)}")
                    return {
                        'statusCode': 401,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            'message': 'Invalid authentication data',
                            'error_type': 'invalid_user_data'
                        })
                    }
                
                user_role = user_payload.get('role')
                if not user_role:
                    logger.warning(f"User payload missing role: {user_payload}")
                    return {
                        'statusCode': 403,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            'message': 'User role not found',
                            'error_type': 'missing_role'
                        })
                    }
                
                if user_role not in allowed_roles:
                    logger.warning(f"User role '{user_role}' not in allowed roles: {allowed_roles}")
                    return {
                        'statusCode': 403,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({
                            'message': f'Access denied. Required role: {", ".join(allowed_roles)}. Your role: {user_role}',
                            'error_type': 'insufficient_permissions'
                        })
                    }
                
                return handler_function(event, context)
                
            except Exception as e:
                logger.error(f"Authorization error in require_role: {str(e)}")
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'message': 'Internal authorization error',
                        'error_type': 'auth_error'
                    })
                }
        
        return wrapper
    
    return decorator

def current_user(func: Callable):
    """
    Decorator to extract the current logged-in user and add it to the function arguments.
    
    This decorator can be used with or without authentication.
    
    Args:
        func: The function to be decorated
        
    Returns:
        Wrapped function with optional current user added as an argument
    """
    @wraps(func)
    def wrapper(event, context, *args, **kwargs):
        # Try to get the user from the token
        current_user = None
        
        try:
            # Check for authorization header (case-insensitive)
            headers = event.get('headers', {})
            auth_header = headers.get('authorization') or headers.get('Authorization')
            
            if auth_header and auth_header.startswith('Bearer '):
                # Extract and verify token
                token = auth_header.split(' ')[1]
                if token:
                    payload, error = verify_token(token)
                    
                    # If token is valid, find the user
                    if payload and not error:
                        user_identifier = payload.get('sub') or payload.get('user_id')
                        if user_identifier:
                            if '@' in str(user_identifier):
                                current_user = find_user(email=user_identifier)
                            else:
                                try:
                                    user_id = int(user_identifier)
                                    current_user = find_user(id=user_id)
                                except (ValueError, TypeError):
                                    current_user = find_user(email=user_identifier)
        except Exception as e:
            # If any error occurs during token verification or user lookup, 
            # we'll just continue without a user
            logger.debug(f"Optional user extraction failed: {str(e)}")
        
        # Add current_user to kwargs, which will be None if no valid user found
        kwargs['current_user'] = current_user
        
        # Call the original function
        return func(event, context, *args, **kwargs)
    
    return wrapper

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