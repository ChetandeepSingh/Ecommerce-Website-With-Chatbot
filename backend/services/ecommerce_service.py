from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from models import User, Order, OrderItem, InventoryItem, DistributionCenter
from schemas import TopProductResponse, OrderStatusResponse, StockLevelResponse
from typing import List, Optional, Dict, Any
import re

class EcommerceService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_top_products(self, limit: int = 5) -> List[TopProductResponse]:
        """Get top selling products by revenue"""
        # Query to get top products by total sales
        top_products = self.db.query(
            InventoryItem.product_name,
            func.count(InventoryItem.id).label('total_sold'),
            func.sum(InventoryItem.product_retail_price).label('revenue')
        ).filter(
            InventoryItem.sold_at.isnot(None)
        ).group_by(
            InventoryItem.product_name
        ).order_by(
            desc('revenue')
        ).limit(limit).all()
        
        return [
            TopProductResponse(
                product_name=product.product_name,
                total_sold=product.total_sold,
                revenue=float(product.revenue) if product.revenue else 0.0
            )
            for product in top_products
        ]
    
    def get_order_status(self, order_id: int) -> Optional[OrderStatusResponse]:
        """Get detailed order status by order ID"""
        order = self.db.query(Order).filter(Order.order_id == order_id).first()
        
        if not order:
            return None
        
        # Get user name if available
        user_name = None
        if order.user_id:
            user = self.db.query(User).filter(User.id == order.user_id).first()
            if user:
                user_name = f"{user.first_name} {user.last_name}"
        
        # Get items count
        items_count = self.db.query(OrderItem).filter(OrderItem.order_id == order_id).count()
        
        return OrderStatusResponse(
            order_id=order.order_id,
            status=order.status,
            user_name=user_name,
            items_count=items_count,
            created_at=order.created_at,
            shipped_at=order.shipped_at,
            delivered_at=order.delivered_at
        )
    
    def get_stock_levels(self, product_name: str = None) -> List[StockLevelResponse]:
        """Get stock levels for products"""
        query = self.db.query(
            InventoryItem.product_name,
            func.count(InventoryItem.id).label('total_inventory'),
            func.count(InventoryItem.sold_at).label('sold_count'),
            InventoryItem.product_category,
            InventoryItem.product_brand
        ).group_by(
            InventoryItem.product_name,
            InventoryItem.product_category,
            InventoryItem.product_brand
        )
        
        if product_name:
            query = query.filter(InventoryItem.product_name.ilike(f"%{product_name}%"))
        
        results = query.all()
        
        return [
            StockLevelResponse(
                product_name=result.product_name,
                available_stock=result.total_inventory - result.sold_count,
                total_inventory=result.total_inventory,
                product_category=result.product_category,
                product_brand=result.product_brand
            )
            for result in results
        ]
    
    def get_user_orders(self, user_id: int) -> List[Order]:
        """Get all orders for a specific user"""
        return self.db.query(Order).filter(Order.user_id == user_id).order_by(desc(Order.created_at)).all()
    
    def get_product_details(self, product_name: str) -> List[InventoryItem]:
        """Get detailed information about a specific product"""
        return self.db.query(InventoryItem).filter(
            InventoryItem.product_name.ilike(f"%{product_name}%")
        ).all()
    
    def get_recent_orders(self, limit: int = 10) -> List[Order]:
        """Get recent orders"""
        return self.db.query(Order).order_by(desc(Order.created_at)).limit(limit).all()
    
    def get_orders_by_status(self, status: str) -> List[Order]:
        """Get orders by status"""
        return self.db.query(Order).filter(Order.status == status).all()
    
    def get_inventory_by_category(self, category: str) -> List[InventoryItem]:
        """Get inventory items by category"""
        return self.db.query(InventoryItem).filter(
            InventoryItem.product_category.ilike(f"%{category}%")
        ).all()
    
    def get_distribution_centers(self) -> List[DistributionCenter]:
        """Get all distribution centers"""
        return self.db.query(DistributionCenter).all()
    
    def get_sales_analytics(self) -> Dict[str, Any]:
        """Get overall sales analytics"""
        total_orders = self.db.query(Order).count()
        total_revenue = self.db.query(func.sum(InventoryItem.product_retail_price)).filter(
            InventoryItem.sold_at.isnot(None)
        ).scalar() or 0
        
        total_customers = self.db.query(User).count()
        total_products = self.db.query(InventoryItem.product_name).distinct().count()
        
        return {
            "total_orders": total_orders,
            "total_revenue": float(total_revenue),
            "total_customers": total_customers,
            "total_products": total_products
        } 