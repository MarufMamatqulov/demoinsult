"""
This module provides a fix for the OpenAI API integration, updating it to work with
both the legacy OpenAI API (< 1.0.0) and the new OpenAI API (>= 1.0.0).
"""

import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)

# Try to load variables from .env file
try:
    # Try to load from project root .env and then from backend/.env
    load_dotenv()
except Exception as e:
    logging.warning(f"Error loading .env file: {str(e)}")

# Try to import the new OpenAI client
try:
    from openai import OpenAI
    USING_NEW_CLIENT = True
    logging.info("Using new OpenAI client (>= 1.0.0)")
except ImportError:
    USING_NEW_CLIENT = False
    import openai
    logging.info("Using legacy OpenAI client (< 1.0.0)")

def get_openai_key():
    """Get the OpenAI API key from environment variables."""
    # Get the key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    
    # If not found, try to load it directly from the .env file
    if not api_key:
        try:
            # Try to load from backend/.env
            backend_env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
            if os.path.exists(backend_env_path):
                with open(backend_env_path, "r") as f:
                    for line in f:
                        if line.strip().startswith("OPENAI_API_KEY="):
                            api_key = line.strip().split("=", 1)[1].strip()
                            if api_key.startswith('"') and api_key.endswith('"'):
                                api_key = api_key[1:-1]
                            logging.info(f"Successfully loaded API key from {backend_env_path}")
                            break
            
            # If still not found, try project root .env
            if not api_key:
                root_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
                if os.path.exists(root_env_path):
                    with open(root_env_path, "r") as f:
                        for line in f:
                            if line.strip().startswith("OPENAI_API_KEY="):
                                api_key = line.strip().split("=", 1)[1].strip()
                                if api_key.startswith('"') and api_key.endswith('"'):
                                    api_key = api_key[1:-1]
                                logging.info(f"Successfully loaded API key from {root_env_path}")
                                break
        except Exception as e:
            logging.error(f"Error reading .env file: {str(e)}")
    
    if not api_key:
        # For development environments, use a placeholder key
        logging.warning("OPENAI_API_KEY is not set in environment variables or .env file. Using placeholder for development. API calls will likely fail with 401 error.")
        placeholder = "sk-placeholder-key-for-development"
        # Set the placeholder in the environment for consistency
        os.environ["OPENAI_API_KEY"] = placeholder
        return placeholder
    
    # Set the API key in the environment to ensure all modules use the same key
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Mask the API key in logs for security
    masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***masked***"
    logging.info(f"Using OpenAI API key: {masked_key}")
    return api_key

def create_chat_completion(messages: List[Dict[str, str]], model: str = "gpt-4o", 
                          temperature: float = 0.7, max_tokens: int = 1000):
    """
    Create a chat completion using either the new or legacy OpenAI API.
    
    Args:
        messages: List of message objects with role and content
        model: The model to use for completion
        temperature: Controls randomness (0 to 1)
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        The generated text response
    """
    api_key = get_openai_key()
    
    try:
        if USING_NEW_CLIENT:
            # Use new OpenAI client (>= 1.0.0)
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        else:
            # Use legacy OpenAI client (< 1.0.0)
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {str(e)}")
        # Check if it's an authentication error
        if "authentication" in str(e).lower() or "api key" in str(e).lower() or "401" in str(e):
            return "I'm having trouble connecting to my knowledge base. This might be due to missing API credentials. Please contact support to ensure API access is properly configured."
        # Return a user-friendly error message
        return "I apologize, but I'm experiencing technical difficulties right now. Please try again later or contact support if the problem persists."
