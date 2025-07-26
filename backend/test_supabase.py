#!/usr/bin/env python3
"""
Test Supabase Connection Script
"""

import os
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_supabase_connection():
    """Test Supabase database connection"""
    # Load environment variables
    load_dotenv()
    
    # Get Supabase connection string
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        logger.error("❌ No DATABASE_URL found in environment variables")
        return False
    
    logger.info("🔗 Testing Supabase connection...")
    logger.info(f"URL: {DATABASE_URL[:30]}..." if len(DATABASE_URL) > 30 else "URL: [configured]")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        logger.info("✅ Engine created successfully")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT NOW()"))
            current_time = result.fetchone()[0]
            logger.info(f"✅ Database connection successful!")
            logger.info(f"   Current database time: {current_time}")
            
        logger.info("🎉 Supabase connection is working!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        logger.info("\n💡 Troubleshooting tips:")
        logger.info("   - Check your .env file has the correct DATABASE_URL")
        logger.info("   - Verify your Supabase password is correct")
        logger.info("   - Make sure your IP is allowed in Supabase settings")
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    exit(0 if success else 1) 