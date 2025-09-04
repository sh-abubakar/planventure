#!/usr/bin/env python3
"""
Database initialization script for PlanVenture API
Run this script to create database tables
"""

from app import app, db
from models.user import User
from models.trip import Trip

def init_database():
    """Initialize the database with all tables."""
    print("🚀 Starting database initialization...")
    
    try:
        with app.app_context():
            print("📋 Creating database tables...")
            
            # Create all tables
            db.create_all()
            
            print("✅ Database tables created successfully!")
            print("📊 Tables available:")
            
            # List created tables (for verification)
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            for table in tables:
                print(f"   - {table}")
            
            if 'users' in tables:
                print("🎉 User model table created successfully!")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("PlanVenture API - Database Initialization")
    print("=" * 50)
    
    success = init_database()
    
    if success:
        print("\n🎊 Database initialization completed successfully!")
        print("You can now run the Flask app with: python app.py")
    else:
        print("\n💥 Database initialization failed!")
        print("Please check the error messages above.")
    
    print("=" * 50)
