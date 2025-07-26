from typing import List, Dict, Any, Optional
from schemas import TopProductResponse, OrderStatusResponse, StockLevelResponse
from services.query_parser import QueryType

class ResponseFormatter:
    def __init__(self):
        pass
    
    def format_top_products_response(self, products: List[TopProductResponse]) -> str:
        """Format top products response"""
        if not products:
            return "I couldn't find any sales data for products at the moment."
        
        response = "Here are the top selling products:\n\n"
        for i, product in enumerate(products, 1):
            response += f"{i}. **{product.product_name}**\n"
            response += f"   - Total Sold: {product.total_sold} units\n"
            response += f"   - Revenue: ${product.revenue:,.2f}\n\n"
        
        return response.strip()
    
    def format_order_status_response(self, order_status: OrderStatusResponse) -> str:
        """Format order status response"""
        if not order_status:
            return "I couldn't find that order. Please check the order ID and try again."
        
        response = f"**Order #{order_status.order_id} Status:**\n\n"
        response += f"**Status:** {order_status.status.title()}\n"
        
        if order_status.user_name:
            response += f"**Customer:** {order_status.user_name}\n"
        
        response += f"**Items:** {order_status.items_count}\n"
        
        if order_status.created_at:
            response += f"**Ordered:** {order_status.created_at.strftime('%B %d, %Y at %I:%M %p')}\n"
        
        if order_status.shipped_at:
            response += f"**Shipped:** {order_status.shipped_at.strftime('%B %d, %Y at %I:%M %p')}\n"
        
        if order_status.delivered_at:
            response += f"**Delivered:** {order_status.delivered_at.strftime('%B %d, %Y at %I:%M %p')}\n"
        
        return response
    
    def format_stock_levels_response(self, stock_levels: List[StockLevelResponse]) -> str:
        """Format stock levels response"""
        if not stock_levels:
            return "I couldn't find any stock information for that product."
        
        if len(stock_levels) == 1:
            stock = stock_levels[0]
            response = f"**Stock Information for {stock.product_name}:**\n\n"
            response += f"**Available Stock:** {stock.available_stock} units\n"
            response += f"**Total Inventory:** {stock.total_inventory} units\n"
            response += f"**Category:** {stock.product_category}\n"
            response += f"**Brand:** {stock.product_brand}\n"
        else:
            response = "I found multiple products matching your query. Here are the stock levels:\n\n"
            for stock in stock_levels:
                response += f"**{stock.product_name}**\n"
                response += f"  - Available: {stock.available_stock} units\n"
                response += f"  - Category: {stock.product_category}\n"
                response += f"  - Brand: {stock.product_brand}\n\n"
        
        return response.strip()
    
    def format_user_orders_response(self, orders: List) -> str:
        """Format user orders response"""
        if not orders:
            return "I couldn't find any orders for that user."
        
        response = f"**Recent Orders:**\n\n"
        for i, order in enumerate(orders[:5], 1):  # Show only last 5 orders
            response += f"{i}. **Order #{order.order_id}**\n"
            response += f"   - Status: {order.status.title()}\n"
            response += f"   - Items: {order.num_of_item}\n"
            if order.created_at:
                response += f"   - Date: {order.created_at.strftime('%B %d, %Y')}\n"
            response += "\n"
        
        if len(orders) > 5:
            response += f"... and {len(orders) - 5} more orders."
        
        return response.strip()
    
    def format_product_details_response(self, products: List) -> str:
        """Format product details response"""
        if not products:
            return "I couldn't find any information about that product."
        
        # Get unique products (group by name)
        unique_products = {}
        for product in products:
            if product.product_name not in unique_products:
                unique_products[product.product_name] = product
        
        response = "**Product Information:**\n\n"
        for product in unique_products.values():
            response += f"**{product.product_name}**\n"
            response += f"  - Category: {product.product_category}\n"
            response += f"  - Brand: {product.product_brand}\n"
            response += f"  - Department: {product.product_department}\n"
            response += f"  - SKU: {product.product_sku}\n"
            response += f"  - Retail Price: ${product.product_retail_price:.2f}\n"
            response += f"  - Cost: ${product.cost:.2f}\n\n"
        
        return response.strip()
    
    def format_sales_analytics_response(self, analytics: Dict[str, Any]) -> str:
        """Format sales analytics response"""
        response = "**Sales Analytics Overview:**\n\n"
        response += f"**Total Orders:** {analytics['total_orders']:,}\n"
        response += f"**Total Revenue:** ${analytics['total_revenue']:,.2f}\n"
        response += f"**Total Customers:** {analytics['total_customers']:,}\n"
        response += f"**Total Products:** {analytics['total_products']:,}\n"
        
        if analytics['total_orders'] > 0:
            avg_order_value = analytics['total_revenue'] / analytics['total_orders']
            response += f"**Average Order Value:** ${avg_order_value:.2f}\n"
        
        return response
    
    def format_general_response(self, message: str) -> str:
        """Format general response for unrecognized queries"""
        response = f"I understand you're asking about: \"{message}\"\n\n"
        response += "I can help you with:\n"
        response += "• **Product information** - Ask about specific products\n"
        response += "• **Order status** - Track orders by ID (e.g., 'order status 12345')\n"
        response += "• **Stock levels** - Check product availability (e.g., 'how many Classic T-Shirts left')\n"
        response += "• **Top products** - See best-selling items (e.g., 'top 5 most sold products')\n"
        response += "• **Sales analytics** - Get business overview\n\n"
        response += "Please try asking in a different way or be more specific!"
        
        return response
    
    def format_error_response(self, error_type: str, details: str = "") -> str:
        """Format error responses"""
        error_messages = {
            "order_not_found": "I couldn't find that order. Please check the order ID and try again.",
            "product_not_found": "I couldn't find that product. Please check the product name and try again.",
            "user_not_found": "I couldn't find that user. Please check the user ID and try again.",
            "database_error": "I'm having trouble accessing the database right now. Please try again later.",
            "invalid_query": "I didn't understand your question. Please try rephrasing it."
        }
        
        base_message = error_messages.get(error_type, "An error occurred. Please try again.")
        if details:
            return f"{base_message}\n\nDetails: {details}"
        return base_message 