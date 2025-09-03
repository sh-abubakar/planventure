from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import db
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

# Initialize extensions
db.init_app(app)
CORS(app)

# Import models
from models.user import User

@app.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({
            "status": "healthy",
            "database": "connected"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
        db.create_all()
    app.run(debug=True)
