from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.user import User
from utils.auth import decode_token, validate_token_format
import jwt

def auth_required(f):
    """
    Decorator to require authentication for a route.
    Uses Flask-JWT-Extended for token verification.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Authentication required', 'error': str(e)}), 401
    return decorated_function

def optional_auth(f):
    """
    Decorator for routes where authentication is optional.
    Provides user info if authenticated, continues if not.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
            return f(*args, **kwargs)
        except Exception:
            # Continue without authentication
            return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to require admin privileges (can be extended for role-based access).
    Currently checks if user exists and is valid.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'message': 'User not found'}), 404
            
            # Add admin role check here when you implement roles
            # if not user.is_admin:
            #     return jsonify({'message': 'Admin privileges required'}), 403
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Admin authentication required', 'error': str(e)}), 401
    return decorated_function

def get_current_user():
    """
    Get the current authenticated user from JWT token.
    Returns User object or None if not authenticated.
    """
    try:
        user_id = get_jwt_identity()
        if user_id:
            return User.query.get(user_id)
        return None
    except:
        return None

def extract_token_from_header():
    """
    Extract JWT token from Authorization header.
    Supports both 'Bearer <token>' and '<token>' formats.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    # Handle 'Bearer <token>' format
    if auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]
    
    # Handle direct token format
    return auth_header

def validate_token_middleware():
    """
    Middleware function to validate JWT token format and expiration.
    Can be used in before_request hooks.
    """
    # Skip validation for auth routes and public routes
    exempt_paths = ['/api/auth/login', '/api/auth/register', '/', '/health']
    
    if request.path in exempt_paths:
        return None
    
    # Skip if no Authorization header
    if 'Authorization' not in request.headers:
        return None
    
    token = extract_token_from_header()
    if not token:
        return jsonify({'message': 'Invalid token format'}), 401
    
    # Validate token format
    if not validate_token_format(token):
        return jsonify({'message': 'Invalid token format'}), 401
    
    # Validate token signature and expiration
    try:
        decoded = decode_token(token)
        if not decoded:
            return jsonify({'message': 'Invalid or expired token'}), 401
    except Exception as e:
        return jsonify({'message': 'Token validation failed', 'error': str(e)}), 401
    
    return None

def require_user_ownership(user_id_field='user_id'):
    """
    Decorator to ensure the authenticated user can only access their own resources.
    
    Args:
        user_id_field: The field name in request data or URL params that contains user_id
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                
                # Get user_id from URL parameters or request data
                resource_user_id = None
                
                # Check URL parameters first
                if user_id_field in kwargs:
                    resource_user_id = int(kwargs[user_id_field])
                
                # Check request JSON data
                elif request.is_json:
                    data = request.get_json()
                    if data and user_id_field in data:
                        resource_user_id = int(data[user_id_field])
                
                # Check query parameters
                elif user_id_field in request.args:
                    resource_user_id = int(request.args.get(user_id_field))
                
                if resource_user_id is None:
                    return jsonify({'message': f'Missing {user_id_field} parameter'}), 400
                
                if current_user_id != resource_user_id:
                    return jsonify({'message': 'Access denied: You can only access your own resources'}), 403
                
                return f(*args, **kwargs)
            except ValueError:
                return jsonify({'message': f'Invalid {user_id_field} format'}), 400
            except Exception as e:
                return jsonify({'message': 'Authorization failed', 'error': str(e)}), 401
        return decorated_function
    return decorator

def rate_limit_by_user(max_requests=100, window_minutes=60):
    """
    Decorator for rate limiting by authenticated user.
    This is a basic implementation - for production use Redis or similar.
    
    Args:
        max_requests: Maximum requests allowed in the time window
        window_minutes: Time window in minutes
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                
                # Basic rate limiting logic would go here
                # For production, implement with Redis or database
                # This is just a placeholder for the structure
                
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'message': 'Rate limiting failed', 'error': str(e)}), 429
        return decorated_function
    return decorator
