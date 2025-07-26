#!/usr/bin/env python3
"""
Test Supabase Connection Script
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase connection string
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"🔗 Testing Supabase connection...")
print(f"URL: {DATABASE_URL[:50]}..." if DATABASE_URL else "❌ No DATABASE_URL found")

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    print("✅ Engine created successfully")
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW()"))
        current_time = result.fetchone()[0]
        print(f"✅ Database connection successful!")
        print(f"   Current database time: {current_time}")
        
    print("🎉 Supabase connection is working!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\n💡 Troubleshooting tips:")
    print("   - Check your .env file has the correct DATABASE_URL")
    print("   - Verify your Supabase password is correct")
    print("   - Make sure your IP is allowed in Supabase settings") 