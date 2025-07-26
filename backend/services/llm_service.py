import os
import json
from typing import Dict, Any, List, Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama3-8b-8192"  # Using Llama3 model for good performance
    
    def generate_response(self, user_message: str, context: Dict[str, Any] = None) -> str:
        """
        Generate an intelligent response using Groq API
        """
        # Build the system prompt
        system_prompt = self._build_system_prompt(context)
        
        # Create the conversation
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return self._get_fallback_response(user_message)
    
    def ask_clarifying_question(self, user_message: str, missing_info: List[str]) -> str:
        """
        Generate a clarifying question when information is missing
        """
        system_prompt = """You are a helpful e-commerce customer support assistant. 
        The user has asked a question but we need more information to help them properly.
        Generate a friendly, helpful clarifying question to get the missing information.
        Be specific and helpful."""
        
        user_prompt = f"""
        User message: "{user_message}"
        
        Missing information: {', '.join(missing_info)}
        
        Please ask a clarifying question to get the missing information. Be friendly and helpful.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error calling Groq API for clarifying question: {e}")
            return f"I'd be happy to help! Could you please provide more details about {', '.join(missing_info)}?"
    
    def enhance_response(self, base_response: str, user_message: str, context: Dict[str, Any] = None) -> str:
        """
        Enhance a base response with additional context and personalization
        """
        system_prompt = """You are a helpful e-commerce customer support assistant.
        You have a base response to give to the user, but you should enhance it to be more helpful, 
        friendly, and personalized. Add relevant suggestions, follow-up questions, or additional helpful information.
        Keep the response conversational and engaging."""
        
        user_prompt = f"""
        User message: "{user_message}"
        
        Base response: "{base_response}"
        
        Context: {json.dumps(context) if context else 'None'}
        
        Please enhance this response to be more helpful and engaging while keeping the core information.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error calling Groq API for response enhancement: {e}")
            return base_response
    
    def _build_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """
        Build the system prompt with context about the e-commerce system
        """
        base_prompt = """You are a helpful e-commerce customer support assistant for a clothing store.
        
        You can help customers with:
        - Product information and availability
        - Order status and tracking
        - Stock levels and inventory
        - Sales analytics and top products
        - General customer support questions
        
        Always be friendly, helpful, and professional. If you don't have enough information to answer a question,
        ask clarifying questions to get the details you need.
        
        When providing information, be specific and accurate. If you're not sure about something, say so rather than guessing."""
        
        if context:
            context_str = json.dumps(context, indent=2)
            base_prompt += f"\n\nCurrent context: {context_str}"
        
        return base_prompt
    
    def _get_fallback_response(self, user_message: str) -> str:
        """
        Provide a fallback response when the API is unavailable
        """
        return f"I understand you're asking about: '{user_message}'. I'm having trouble accessing my advanced features right now, but I can still help you with basic information. Could you please try rephrasing your question or ask about something specific like order status, product availability, or sales information?"
    
    def is_api_available(self) -> bool:
        """
        Check if the Groq API is available
        """
        try:
            # Simple test call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True
        except Exception:
            return False 