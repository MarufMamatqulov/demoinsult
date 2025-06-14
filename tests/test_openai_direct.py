import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Get API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    print(f"Using OpenAI API key: {api_key[:8]}...{api_key[-4:]}")
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Make a test request
    try:
        print("Sending test request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, API is working correctly!' in a short response."}
            ],
            max_tokens=50
        )
        
        print("\nResponse from OpenAI API:")
        print(response.choices[0].message.content)
        print("\nAPI test successful!")
        return True
    except Exception as e:
        print(f"\nError calling OpenAI API: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
