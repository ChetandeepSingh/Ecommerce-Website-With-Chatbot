#!/usr/bin/env python3
"""
Supabase Database Setup Script
Creates all tables in Supabase PostgreSQL database
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase connection string
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"🚀 Setting up Supabase database...")

def create_tables():
    """Create all database tables"""
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def test_tables():
    """Test that tables were created"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Check if tables exist
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result.fetchall()]
            
            print(f"📋 Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table}")
            
            return True
    except Exception as e:
        print(f"❌ Failed to test tables: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Supabase Database Setup...\n")
    
    # Step 1: Create tables
    if not create_tables():
        return False
    
    # Step 2: Test tables
    if not test_tables():
        return False
    
    print("\n🎉 Supabase database setup completed successfully!")
    print("   You can now view your tables in the Supabase dashboard")
    print("   Next step: Load data from CSV files")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 