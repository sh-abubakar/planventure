# Planventure API 🌍

A Flask-based REST API for travel planning and trip management with JWT authentication, SQLAlchemy ORM, and comprehensive CRUD operations.

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Endpoints](#-api-endpoints)
- [Authentication](#-authentication)
- [Database Models](#-database-models)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

## ✨ Features

- **User Authentication**: Secure JWT-based authentication with registration and login
- **Trip Management**: Full CRUD operations for travel trips
- **Automatic Itinerary Generation**: Smart itinerary templates based on destination and trip type
- **Coordinate Support**: GPS coordinates for trip locations
- **CORS Enabled**: Ready for React frontend integration
- **Database Migrations**: Flask-Migrate support for schema changes
- **Password Security**: Bcrypt hashing with salt
- **Input Validation**: Comprehensive data validation and error handling

## 🛠 Technology Stack

- **Framework**: Flask 2.3.3
- **Database**: SQLAlchemy 3.1.1 with SQLite (default)
- **Authentication**: Flask-JWT-Extended 4.5.3
- **Password Hashing**: Bcrypt 4.0.1
- **CORS**: Flask-CORS 4.0.0
- **Environment Management**: Python-dotenv 1.0.0
- **Production Server**: Gunicorn 21.2.0

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Local Development Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd planventure/planventure-api
```

2. **Create and activate virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .sample.env .env
```

5. **Initialize the database**:
```bash
python init_db.py
```

6. **Start the development server**:
```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on [`.sample.env`](.sample.env):

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///planventure.db

# Frontend Configuration
FRONTEND_URL=http://localhost:3000

# Development Settings
FLASK_ENV=development
DEBUG=True
```

### Database Configuration

The API supports multiple database backends through SQLAlchemy:

- **SQLite** (default): `sqlite:///planventure.db`
- **PostgreSQL**: `postgresql://user:password@localhost/planventure`
- **MySQL**: `mysql://user:password@localhost/planventure`

## 📡 API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check with database status |
| GET | `/cors-test` | CORS configuration test |

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | User registration |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/refresh` | Refresh access token |
| GET | `/api/auth/me` | Get current user info |
| POST | `/api/auth/logout` | User logout |
| POST | `/api/auth/check-email` | Check email availability |

### Trip Endpoints (Protected)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trips/` | Get all user trips |
| POST | `/api/trips/` | Create new trip |
| GET | `/api/trips/{id}` | Get specific trip |
| PUT | `/api/trips/{id}` | Update trip |
| DELETE | `/api/trips/{id}` | Delete trip |
| POST | `/api/trips/itinerary-suggestions` | Get itinerary suggestions |
| POST | `/api/trips/generate-itinerary` | Generate custom itinerary |

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

### Registration

```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Login

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Using Protected Endpoints

Include the JWT token in the Authorization header:

```bash
curl -X GET http://127.0.0.1:5000/api/trips/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🗃️ Database Models

### User Model

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Trip Model

```python
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    itinerary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## 🔧 Development

### Project Structure

```
planventure-api/
├── app.py                 # Main Flask application
├── database.py           # Database configuration
├── init_db.py            # Database initialization script
├── requirements.txt      # Python dependencies
├── .sample.env          # Environment variables template
├── models/              # Database models
│   ├── __init__.py
│   ├── user.py         # User model
│   └── trip.py         # Trip model
├── routes/              # API route blueprints
│   ├── auth.py         # Authentication routes
│   └── trips.py        # Trip management routes
└── utils/               # Utility functions
    ├── auth.py         # JWT utilities
    ├── password.py     # Password hashing
    ├── middleware.py   # Authentication middleware
    └── itinerary.py    # Itinerary generation
```

### Development Commands

**Start development server**:
```bash
python app.py
```

**Initialize/Reset database**:
```bash
python init_db.py
```

**Install new dependencies**:
```bash
pip install package_name
pip freeze > requirements.txt
```

### Code Style

The project follows Python best practices:
- PEP 8 style guidelines
- Comprehensive error handling
- Input validation and sanitization
- Secure password handling
- JWT token management

## 🧪 Testing

### Manual Testing

Use the provided test examples in [`TRIP_TESTING_EXAMPLES.md`](TRIP_TESTING_EXAMPLES.md):

1. **Register a test user**
2. **Login to get JWT tokens**
3. **Test trip CRUD operations**
4. **Test itinerary generation**

### API Testing Tools

- **Bruno**: Recommended API client
- **Postman**: Alternative API testing
- **curl**: Command-line testing
- **HTTPie**: User-friendly HTTP client

### Sample Trip Creation

```bash
curl -X POST http://127.0.0.1:5000/api/trips/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris, France",
    "start_date": "2024-10-15",
    "end_date": "2024-10-22",
    "latitude": 48.8566,
    "longitude": 2.3522
  }'
```

## 🚀 Deployment

### Production Configuration

1. **Set production environment variables**:
```env
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret
DATABASE_URL=postgresql://user:pass@host:5432/dbname
FRONTEND_URL=https://your-frontend-domain.com
FLASK_ENV=production
DEBUG=False
```

2. **Use production database**:
   - PostgreSQL (recommended)
   - MySQL
   - SQLite (development only)

3. **Deploy with Gunicorn**:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Support

The project includes `.devcontainer` configuration for development with Docker and PostgreSQL.

### Security Considerations

- Use strong SECRET_KEY and JWT_SECRET_KEY
- Enable HTTPS in production
- Configure proper CORS origins
- Use environment variables for secrets
- Regularly update dependencies
- Implement rate limiting for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test your changes
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Create a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comprehensive error handling
- Include docstrings for functions
- Test your changes thoroughly
- Update documentation as needed

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [React Integration Guide](REACT_INTEGRATION.md)
- [API Testing Examples](TRIP_TESTING_EXAMPLES.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

For support, please:
1. Check the [documentation](README.md)
2. Review [testing examples](TRIP_TESTING_EXAMPLES.md)
3. Open an issue on GitHub
4. Contact the maintainers

---

**Happy Traveling! 🌍✈️**