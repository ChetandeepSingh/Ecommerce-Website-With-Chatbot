#!/usr/bin/env python3
"""
Supabase Data Loading Script
Loads CSV data into Supabase PostgreSQL database
"""

import pandas as pd
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, DistributionCenter, User, InventoryItem, Order, OrderItem
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase connection string
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"🚀 Loading data into Supabase...")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_distribution_centers():
    """Load distribution centers data"""
    print("📦 Loading distribution centers...")
    csv_path = os.path.join('..', 'dataset', 'archive', 'distribution_centers.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        db = SessionLocal()
        
        for _, row in df.iterrows():
            distribution_center = DistributionCenter(
                id=row['id'],
                name=row['name'],
                latitude=row['latitude'],
                longitude=row['longitude']
            )
            db.add(distribution_center)
        
        db.commit()
        db.close()
        print(f"✅ Loaded {len(df)} distribution centers")
        return True
        
    except Exception as e:
        print(f"❌ Error loading distribution centers: {e}")
        return False

def load_users():
    """Load users data"""
    print("👥 Loading users...")
    csv_path = os.path.join('..', 'dataset', 'archive', 'users.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return False
    
    try:
        # Read in chunks to handle large files
        chunk_size = 1000
        total_loaded = 0
        db = SessionLocal()
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            for _, row in chunk.iterrows():
                user = User(
                    id=row['id'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    age=row['age'] if pd.notna(row['age']) else None,
                    gender=row['gender'] if pd.notna(row['gender']) else None,
                    state=row['state'] if pd.notna(row['state']) else None,
                    street_address=row['street_address'] if pd.notna(row['street_address']) else None,
                    postal_code=row['postal_code'] if pd.notna(row['postal_code']) else None,
                    city=row['city'] if pd.notna(row['city']) else None,
                    country=row['country'] if pd.notna(row['country']) else None,
                    latitude=row['latitude'] if pd.notna(row['latitude']) else None,
                    longitude=row['longitude'] if pd.notna(row['longitude']) else None,
                    traffic_source=row['traffic_source'] if pd.notna(row['traffic_source']) else None,
                    created_at=pd.to_datetime(row['created_at']) if pd.notna(row['created_at']) else None
                )
                db.add(user)
            
            db.commit()
            total_loaded += len(chunk)
            print(f"   Loaded {total_loaded} users so far...")
        
        db.close()
        print(f"✅ Total users loaded: {total_loaded}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading users: {e}")
        return False

def load_inventory_items():
    """Load inventory items data"""
    print("📦 Loading inventory items...")
    csv_path = os.path.join('..', 'dataset', 'archive', 'inventory_items.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return False
    
    try:
        # Read in chunks to handle large files
        chunk_size = 1000
        total_loaded = 0
        db = SessionLocal()
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            for _, row in chunk.iterrows():
                inventory_item = InventoryItem(
                    id=row['id'],
                    product_id=row['product_id'],
                    created_at=pd.to_datetime(row['created_at']) if pd.notna(row['created_at']) else None,
                    sold_at=pd.to_datetime(row['sold_at']) if pd.notna(row['sold_at']) else None,
                    cost=row['cost'],
                    product_category=row['product_category'],
                    product_name=row['product_name'],
                    product_brand=row['product_brand'] if pd.notna(row['product_brand']) else 'Unknown',
                    product_retail_price=row['product_retail_price'],
                    product_department=row['product_department'],
                    product_sku=row['product_sku'],
                    product_distribution_center_id=row['product_distribution_center_id'] if pd.notna(row['product_distribution_center_id']) else None
                )
                db.add(inventory_item)
            
            db.commit()
            total_loaded += len(chunk)
            print(f"   Loaded {total_loaded} inventory items so far...")
        
        db.close()
        print(f"✅ Total inventory items loaded: {total_loaded}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading inventory items: {e}")
        return False

def load_orders():
    """Load orders data"""
    print("📋 Loading orders...")
    csv_path = os.path.join('..', 'dataset', 'archive', 'orders.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return False
    
    try:
        # Read in chunks to handle large files
        chunk_size = 1000
        total_loaded = 0
        db = SessionLocal()
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            for _, row in chunk.iterrows():
                order = Order(
                    order_id=row['order_id'],
                    user_id=row['user_id'] if pd.notna(row['user_id']) else None,
                    status=row['status'],
                    gender=row['gender'] if pd.notna(row['gender']) else None,
                    created_at=pd.to_datetime(row['created_at']) if pd.notna(row['created_at']) else None,
                    returned_at=pd.to_datetime(row['returned_at']) if pd.notna(row['returned_at']) else None,
                    shipped_at=pd.to_datetime(row['shipped_at']) if pd.notna(row['shipped_at']) else None,
                    delivered_at=pd.to_datetime(row['delivered_at']) if pd.notna(row['delivered_at']) else None,
                    num_of_item=row['num_of_item']
                )
                db.add(order)
            
            db.commit()
            total_loaded += len(chunk)
            print(f"   Loaded {total_loaded} orders so far...")
        
        db.close()
        print(f"✅ Total orders loaded: {total_loaded}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading orders: {e}")
        return False

def load_order_items():
    """Load order items data"""
    print("📦 Loading order items...")
    csv_path = os.path.join('..', 'dataset', 'archive', 'order_items.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return False
    
    try:
        # Read in chunks to handle large files
        chunk_size = 1000
        total_loaded = 0
        db = SessionLocal()
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            for _, row in chunk.iterrows():
                order_item = OrderItem(
                    id=row['id'],
                    order_id=row['order_id'],
                    user_id=row['user_id'] if pd.notna(row['user_id']) else None,
                    product_id=row['product_id'],
                    inventory_item_id=row['inventory_item_id'] if pd.notna(row['inventory_item_id']) else None,
                    status=row['status'],
                    created_at=pd.to_datetime(row['created_at']) if pd.notna(row['created_at']) else None,
                    shipped_at=pd.to_datetime(row['shipped_at']) if pd.notna(row['shipped_at']) else None,
                    delivered_at=pd.to_datetime(row['delivered_at']) if pd.notna(row['delivered_at']) else None,
                    returned_at=pd.to_datetime(row['returned_at']) if pd.notna(row['returned_at']) else None
                )
                db.add(order_item)
            
            db.commit()
            total_loaded += len(chunk)
            print(f"   Loaded {total_loaded} order items so far...")
        
        db.close()
        print(f"✅ Total order items loaded: {total_loaded}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading order items: {e}")
        return False

def main():
    """Main data loading function"""
    print("🚀 Starting data loading process...\n")
    
    # Load data in order (respecting foreign key constraints)
    success = True
    
    if not load_distribution_centers():
        success = False
    
    if not load_users():
        success = False
    
    if not load_inventory_items():
        success = False
    
    if not load_orders():
        success = False
    
    if not load_order_items():
        success = False
    
    if success:
        print("\n🎉 Data loading completed successfully!")
        print("   You can now view your data in the Supabase dashboard")
        print("   Next step: Test the chatbot API")
    else:
        print("\n⚠️  Some data loading failed, but the system should still work")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 