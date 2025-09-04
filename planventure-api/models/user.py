from datetime import datetime
from database import db
from utils.password import hash_password, verify_password

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password: str) -> None:
        """Set the user's password hash."""
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hash."""
        return verify_password(password, self.password_hash)

    def to_dict(self) -> dict:
        """Convert user to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
