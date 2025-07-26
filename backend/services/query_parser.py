import re
from typing import Dict, Any, Optional, List
from enum import Enum

class QueryType(str, Enum):
    TOP_PRODUCTS = "top_products"
    ORDER_STATUS = "order_status"
    STOCK_LEVELS = "stock_levels"
    USER_ORDERS = "user_orders"
    PRODUCT_DETAILS = "product_details"
    SALES_ANALYTICS = "sales_analytics"
    GENERAL = "general"

class QueryParser:
    def __init__(self):
        # Patterns for different types of queries
        self.patterns = {
            QueryType.TOP_PRODUCTS: [
                r"top\s+(\d+)?\s*(?:most\s+)?(?:sold|popular|best\s+selling)\s+products?",
                r"(?:what\s+are\s+)?(?:the\s+)?(?:top\s+)?(\d+)?\s*(?:most\s+)?(?:sold|popular|best\s+selling)\s+products?",
                r"best\s+selling\s+products?",
                r"most\s+popular\s+products?"
            ],
            QueryType.ORDER_STATUS: [
                r"order\s+(?:status|information)\s+(?:for\s+)?(?:order\s+)?(?:id\s+)?(\d+)",
                r"status\s+of\s+order\s+(?:id\s+)?(\d+)",
                r"show\s+me\s+(?:the\s+)?(?:status\s+of\s+)?order\s+(?:id\s+)?(\d+)",
                r"where\s+is\s+my\s+order\s+(?:id\s+)?(\d+)",
                r"track\s+order\s+(?:id\s+)?(\d+)"
            ],
            QueryType.STOCK_LEVELS: [
                r"(?:how\s+many|what\s+is\s+the\s+stock|stock\s+level)\s+(?:of\s+)?(.+?)\s+(?:left\s+)?(?:in\s+stock|available)?",
                r"stock\s+(?:level|quantity)\s+(?:of\s+)?(.+?)",
                r"available\s+stock\s+(?:of\s+)?(.+?)",
                r"(.+?)\s+(?:stock|inventory|available)"
            ],
            QueryType.USER_ORDERS: [
                r"my\s+orders?",
                r"orders?\s+(?:for\s+)?(?:user\s+)?(?:id\s+)?(\d+)",
                r"customer\s+(\d+)\s+orders?"
            ],
            QueryType.PRODUCT_DETAILS: [
                r"product\s+(?:details|information)\s+(?:for\s+)?(.+?)",
                r"tell\s+me\s+about\s+(?:the\s+)?(.+?)",
                r"what\s+is\s+(?:the\s+)?(.+?)",
                r"(.+?)\s+(?:product|item|details)"
            ],
            QueryType.SALES_ANALYTICS: [
                r"sales?\s+(?:analytics|statistics|summary|overview)",
                r"business\s+(?:analytics|statistics|summary)",
                r"overall\s+(?:sales|business)\s+(?:performance|statistics)",
                r"company\s+(?:performance|statistics|analytics)"
            ]
        }
    
    def parse_query(self, user_message: str) -> Dict[str, Any]:
        """
        Parse user message and extract query type and parameters
        """
        user_message = user_message.lower().strip()
        
        # Check each query type pattern
        for query_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_message, re.IGNORECASE)
                if match:
                    params = self._extract_parameters(query_type, match, user_message)
                    return {
                        "query_type": query_type,
                        "parameters": params,
                        "confidence": 0.9
                    }
        
        # If no specific pattern matches, return general query
        return {
            "query_type": QueryType.GENERAL,
            "parameters": {"message": user_message},
            "confidence": 0.1
        }
    
    def _extract_parameters(self, query_type: QueryType, match: re.Match, full_message: str) -> Dict[str, Any]:
        """Extract parameters based on query type"""
        params = {}
        
        if query_type == QueryType.TOP_PRODUCTS:
            # Extract number if specified
            if match.group(1):
                params["limit"] = int(match.group(1))
            else:
                params["limit"] = 5
        
        elif query_type == QueryType.ORDER_STATUS:
            # Extract order ID
            params["order_id"] = int(match.group(1))
        
        elif query_type == QueryType.STOCK_LEVELS:
            # Extract product name
            product_name = match.group(1).strip()
            # Clean up the product name
            product_name = re.sub(r'\s+(?:left\s+)?(?:in\s+stock|available)?$', '', product_name)
            params["product_name"] = product_name
        
        elif query_type == QueryType.USER_ORDERS:
            # Extract user ID if specified
            if match.group(1):
                params["user_id"] = int(match.group(1))
        
        elif query_type == QueryType.PRODUCT_DETAILS:
            # Extract product name
            product_name = match.group(1).strip()
            params["product_name"] = product_name
        
        return params
    
    def get_response_template(self, query_type: QueryType) -> str:
        """Get response template for different query types"""
        templates = {
            QueryType.TOP_PRODUCTS: "Here are the top {limit} most sold products:",
            QueryType.ORDER_STATUS: "Order status for order #{order_id}:",
            QueryType.STOCK_LEVELS: "Stock levels for {product_name}:",
            QueryType.USER_ORDERS: "Orders for user {user_id}:",
            QueryType.PRODUCT_DETAILS: "Product details for {product_name}:",
            QueryType.SALES_ANALYTICS: "Here are the overall sales analytics:",
            QueryType.GENERAL: "I understand you're asking about: {message}. Let me help you with that."
        }
        return templates.get(query_type, "I'll help you with that.") 