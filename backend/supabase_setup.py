#!/usr/bin/env python3
"""
Supabase Database Setup Script
Creates all tables in Supabase PostgreSQL database
"""

import os
import logging
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_environment():
    """Validate environment setup"""
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        logger.error("❌ DATABASE_URL environment variable is not set")
        logger.error("   Please check your .env file")
        return False
    
    logger.info("✅ Environment variables loaded successfully")
    return True

def create_tables():
    """Create all database tables"""
    try:
        DATABASE_URL = os.getenv("DATABASE_URL")
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        return False

def test_tables():
    """Test that tables were created"""
    try:
        DATABASE_URL = os.getenv("DATABASE_URL")
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
            
            logger.info(f"📋 Found {len(tables)} tables:")
            for table in tables:
                logger.info(f"   - {table}")
            
            # Check for required tables
            required_tables = [
                'conversation_messages', 'conversation_sessions', 
                'distribution_centers', 'inventory_items', 
                'order_items', 'orders', 'users'
            ]
            
            missing_tables = [table for table in required_tables if table not in tables]
            if missing_tables:
                logger.warning(f"⚠️  Missing tables: {missing_tables}")
                return False
            
            logger.info("✅ All required tables are present")
            return True
    except Exception as e:
        logger.error(f"❌ Failed to test tables: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("🚀 Supabase Database Setup...\n")
    
    # Step 1: Validate environment
    if not validate_environment():
        return False
    
    # Step 2: Create tables
    if not create_tables():
        return False
    
    # Step 3: Test tables
    if not test_tables():
        return False
    
    logger.info("\n🎉 Supabase database setup completed successfully!")
    logger.info("   You can now view your tables in the Supabase dashboard")
    logger.info("   Next step: Load data from CSV files")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 