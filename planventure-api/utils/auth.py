from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
import jwt
from flask import current_app

def generate_tokens(user_id: int) -> Dict[str, str]:
    """
    Generate access and refresh tokens for a user.
    
    Args:
        user_id: The user's ID
        
    Returns:
        Dictionary containing access_token and refresh_token
    """
    access_token = create_access_token(
        identity=user_id,
        expires_delta=timedelta(hours=1)
    )
    
    refresh_token = create_refresh_token(
        identity=user_id,
        expires_delta=timedelta(days=30)
    )
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: The JWT token to decode
        
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token, 
            current_app.config['JWT_SECRET_KEY'], 
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user_id() -> Optional[int]:
    """
    Get the current user ID from the JWT token.
    
    Returns:
        User ID or None if not authenticated
    """
    try:
        return get_jwt_identity()
    except:
        return None

def create_password_reset_token(user_id: int) -> str:
    """
    Create a password reset token.
    
    Args:
        user_id: The user's ID
        
    Returns:
        Password reset token
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'type': 'password_reset'
    }
    
    return jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )

def verify_password_reset_token(token: str) -> Optional[int]:
    """
    Verify a password reset token and return user ID.
    
    Args:
        token: The password reset token
        
    Returns:
        User ID or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        
        if payload.get('type') != 'password_reset':
            return None
            
        return payload.get('user_id')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def validate_token_format(token: str) -> bool:
    """
    Validate JWT token format without verifying signature.
    
    Args:
        token: The JWT token to validate
        
    Returns:
        True if token format is valid, False otherwise
    """
    try:
        # JWT tokens have 3 parts separated by dots
        parts = token.split('.')
        return len(parts) == 3
    except:
        return False
