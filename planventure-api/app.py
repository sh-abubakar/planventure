from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from database import db
import os
from datetime import timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', os.getenv('SECRET_KEY', 'dev'))
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Configure CORS for React frontend
cors_origins = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",  # Alternative localhost
    "http://localhost:3001",  # Alternative React port
    "http://127.0.0.1:3001",  # Alternative localhost
]

# Add production origins from environment variable
if os.getenv('FRONTEND_URL'):
    cors_origins.append(os.getenv('FRONTEND_URL'))

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app, 
     origins=cors_origins,
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'],
     supports_credentials=True)

# Import models
from models.user import User
from models.trip import Trip

# Import and register blueprints
from routes.auth import auth_bp
from routes.trips import trips_bp
app.register_blueprint(auth_bp)
app.register_blueprint(trips_bp)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@app.route('/health')
def health_check():
    try:
        with app.app_context():
            db.session.execute(db.text('SELECT 1'))
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "cors": "enabled"
            })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500

@app.route('/cors-test', methods=['GET', 'POST', 'OPTIONS'])
def cors_test():
    """Test endpoint to verify CORS configuration."""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight successful'}), 200
    
    return jsonify({
        'message': 'CORS test successful',
        'method': request.method,
        'origin': request.headers.get('Origin', 'No origin header'),
        'user_agent': request.headers.get('User-Agent', 'No user agent'),
        'cors_enabled': True
    }), 200

# Additional CORS headers for React frontend
@app.after_request
def after_request(response):
    """Add additional CORS headers for React frontend compatibility."""
    origin = request.headers.get('Origin')
    
    # Check if origin is in allowed origins
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ]
    
    if os.getenv('FRONTEND_URL'):
        allowed_origins.append(os.getenv('FRONTEND_URL'))
    
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours
    
    return response

# JWT configuration and error handlers
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "Invalid token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message": "Authorization token is required"}), 401

if __name__ == '__main__':
    app.run(debug=True)
