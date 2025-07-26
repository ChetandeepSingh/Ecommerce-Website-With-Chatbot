import pandas as pd
import os
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, DistributionCenter, User, InventoryItem, Order, OrderItem
import sys

# Add the parent directory to the path to import from dataset
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def load_distribution_centers(db: Session):
    """Load distribution centers data"""
    print("Loading distribution centers...")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'archive', 'distribution_centers.csv')
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return
    
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        distribution_center = DistributionCenter(
            id=row['id'],
            name=row['name'],
            latitude=row['latitude'],
            longitude=row['longitude']
        )
        db.add(distribution_center)
    
    db.commit()
    print(f"Loaded {len(df)} distribution centers")

def load_users(db: Session):
    """Load users data"""
    print("Loading users...")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'archive', 'users.csv')
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return
    
    # Read in chunks to handle large files
    chunk_size = 1000
    total_loaded = 0
    
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
        print(f"Loaded {total_loaded} users so far...")
    
    print(f"Total users loaded: {total_loaded}")

def load_inventory_items(db: Session):
    """Load inventory items data"""
    print("Loading inventory items...")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'archive', 'inventory_items.csv')
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return
    
    # Read in chunks to handle large files
    chunk_size = 1000
    total_loaded = 0
    
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
                product_brand=row['product_brand'],
                product_retail_price=row['product_retail_price'],
                product_department=row['product_department'],
                product_sku=row['product_sku'],
                product_distribution_center_id=row['product_distribution_center_id'] if pd.notna(row['product_distribution_center_id']) else None
            )
            db.add(inventory_item)
        
        db.commit()
        total_loaded += len(chunk)
        print(f"Loaded {total_loaded} inventory items so far...")
    
    print(f"Total inventory items loaded: {total_loaded}")

def load_orders(db: Session):
    """Load orders data"""
    print("Loading orders...")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'archive', 'orders.csv')
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return
    
    # Read in chunks to handle large files
    chunk_size = 1000
    total_loaded = 0
    
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
        print(f"Loaded {total_loaded} orders so far...")
    
    print(f"Total orders loaded: {total_loaded}")

def load_order_items(db: Session):
    """Load order items data"""
    print("Loading order items...")
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'archive', 'order_items.csv')
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return
    
    # Read in chunks to handle large files
    chunk_size = 1000
    total_loaded = 0
    
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
        print(f"Loaded {total_loaded} order items so far...")
    
    print(f"Total order items loaded: {total_loaded}")

def main():
    """Main function to load all data"""
    print("Starting data loading process...")
    
    # Create tables
    create_tables()
    print("Database tables created successfully!")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Load data in order (respecting foreign key constraints)
        load_distribution_centers(db)
        load_users(db)
        load_inventory_items(db)
        load_orders(db)
        load_order_items(db)
        
        print("Data loading completed successfully!")
        
    except Exception as e:
        print(f"Error during data loading: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 