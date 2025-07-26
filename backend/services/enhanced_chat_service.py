from typing import Dict, Any, List, Optional, Tuple
from services.ecommerce_service import EcommerceService
from services.query_parser import QueryParser, QueryType
from services.response_formatter import ResponseFormatter
from services.llm_service import LLMService
from sqlalchemy.orm import Session

class EnhancedChatService:
    def __init__(self, db: Session):
        self.db = db
        self.ecommerce_service = EcommerceService(db)
        self.query_parser = QueryParser()
        self.response_formatter = ResponseFormatter()
        
        # Initialize LLM service (with fallback if API key is not available)
        try:
            self.llm_service = LLMService()
            self.llm_available = self.llm_service.is_api_available()
        except Exception as e:
            print(f"LLM service not available: {e}")
            self.llm_service = None
            self.llm_available = False
    
    def process_message(self, user_message: str, conversation_history: List[Dict] = None) -> Tuple[str, bool, List[str]]:
        """
        Process a user message and return response, whether clarification is needed, and missing info
        """
        # Parse the user's query
        parsed_query = self.query_parser.parse_query(user_message)
        query_type = parsed_query["query_type"]
        parameters = parsed_query["parameters"]
        confidence = parsed_query["confidence"]
        
        # Check if we need more information
        missing_info = self._check_missing_information(query_type, parameters)
        
        if missing_info:
            # Ask for clarification
            clarifying_question = self._generate_clarifying_question(user_message, missing_info)
            return clarifying_question, True, missing_info
        
        # Generate response based on query type
        base_response = self._generate_base_response(query_type, parameters)
        
        # Enhance response with LLM if available
        if self.llm_available and self.llm_service:
            try:
                # Build context for LLM
                context = self._build_context(query_type, parameters, base_response)
                
                # Enhance the response
                enhanced_response = self.llm_service.enhance_response(
                    base_response, user_message, context
                )
                return enhanced_response, False, []
            except Exception as e:
                print(f"Error enhancing response with LLM: {e}")
                return base_response, False, []
        else:
            return base_response, False, []
    
    def _check_missing_information(self, query_type: QueryType, parameters: Dict[str, Any]) -> List[str]:
        """Check if we have all the information needed to answer the query"""
        missing_info = []
        
        if query_type == QueryType.ORDER_STATUS:
            if "order_id" not in parameters:
                missing_info.append("order ID")
        
        elif query_type == QueryType.STOCK_LEVELS:
            if "product_name" not in parameters or not parameters["product_name"]:
                missing_info.append("product name")
        
        elif query_type == QueryType.USER_ORDERS:
            if "user_id" not in parameters:
                missing_info.append("user ID")
        
        elif query_type == QueryType.PRODUCT_DETAILS:
            if "product_name" not in parameters or not parameters["product_name"]:
                missing_info.append("product name")
        
        return missing_info
    
    def _generate_clarifying_question(self, user_message: str, missing_info: List[str]) -> str:
        """Generate a clarifying question using LLM or fallback"""
        if self.llm_available and self.llm_service:
            try:
                return self.llm_service.ask_clarifying_question(user_message, missing_info)
            except Exception as e:
                print(f"Error generating clarifying question with LLM: {e}")
        
        # Fallback clarifying question
        if "order ID" in missing_info:
            return "I'd be happy to help you check your order status! Could you please provide your order ID?"
        elif "product name" in missing_info:
            return "I'd be happy to help you with product information! Could you please tell me which product you're interested in?"
        elif "user ID" in missing_info:
            return "I'd be happy to help you check your orders! Could you please provide your user ID?"
        else:
            return f"I'd be happy to help! Could you please provide more details about {', '.join(missing_info)}?"
    
    def _generate_base_response(self, query_type: QueryType, parameters: Dict[str, Any]) -> str:
        """Generate the base response using business logic"""
        try:
            if query_type == QueryType.TOP_PRODUCTS:
                limit = parameters.get("limit", 5)
                products = self.ecommerce_service.get_top_products(limit)
                return self.response_formatter.format_top_products_response(products)
                
            elif query_type == QueryType.ORDER_STATUS:
                order_id = parameters.get("order_id")
                order_status = self.ecommerce_service.get_order_status(order_id)
                return self.response_formatter.format_order_status_response(order_status)
                
            elif query_type == QueryType.STOCK_LEVELS:
                product_name = parameters.get("product_name")
                stock_levels = self.ecommerce_service.get_stock_levels(product_name)
                return self.response_formatter.format_stock_levels_response(stock_levels)
                
            elif query_type == QueryType.USER_ORDERS:
                user_id = parameters.get("user_id")
                orders = self.ecommerce_service.get_user_orders(user_id)
                return self.response_formatter.format_user_orders_response(orders)
                
            elif query_type == QueryType.PRODUCT_DETAILS:
                product_name = parameters.get("product_name")
                products = self.ecommerce_service.get_product_details(product_name)
                return self.response_formatter.format_product_details_response(products)
                
            elif query_type == QueryType.SALES_ANALYTICS:
                analytics = self.ecommerce_service.get_sales_analytics()
                return self.response_formatter.format_sales_analytics_response(analytics)
                
            else:  # QueryType.GENERAL
                message = parameters.get("message", "")
                return self.response_formatter.format_general_response(message)
                
        except Exception as e:
            return self.response_formatter.format_error_response("database_error", str(e))
    
    def _build_context(self, query_type: QueryType, parameters: Dict[str, Any], base_response: str) -> Dict[str, Any]:
        """Build context for LLM enhancement"""
        context = {
            "query_type": query_type.value,
            "parameters": parameters,
            "base_response": base_response,
            "llm_available": self.llm_available
        }
        
        # Add additional context based on query type
        if query_type == QueryType.ORDER_STATUS:
            order_id = parameters.get("order_id")
            if order_id:
                order_status = self.ecommerce_service.get_order_status(order_id)
                if order_status:
                    context["order_details"] = {
                        "status": order_status.status,
                        "items_count": order_status.items_count,
                        "user_name": order_status.user_name
                    }
        
        elif query_type == QueryType.STOCK_LEVELS:
            product_name = parameters.get("product_name")
            if product_name:
                stock_levels = self.ecommerce_service.get_stock_levels(product_name)
                context["stock_info"] = [
                    {
                        "product_name": stock.product_name,
                        "available_stock": stock.available_stock,
                        "category": stock.product_category
                    }
                    for stock in stock_levels
                ]
        
        return context
    
    def get_llm_status(self) -> Dict[str, Any]:
        """Get the status of LLM service"""
        return {
            "available": self.llm_available,
            "service_initialized": self.llm_service is not None
        } 