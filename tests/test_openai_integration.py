import unittest
import sys
import os
from unittest.mock import MagicMock, patch
import json

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.api.openai_integration import router, get_system_prompt, RehabilitationAnalysisRequest, ChatCompletionRequest

class TestOpenAIIntegration(unittest.TestCase):
    
    def setUp(self):
        self.mock_openai_response = MagicMock()
        self.mock_openai_response.choices = [MagicMock()]
        self.mock_openai_response.choices[0].message = {"content": "This is a mock AI response with some recommendations.\n- First recommendation\n- Second recommendation"}
    
    @patch('backend.api.openai_integration.openai.ChatCompletion.create')
    async def test_analyze_rehabilitation_data(self, mock_openai_create):
        # Set up mock response
        mock_openai_create.return_value = self.mock_openai_response
        
        # Test request
        request = RehabilitationAnalysisRequest(
            assessment_data={"q1": 2, "q2": 1, "q3": 3},
            assessment_type="nihss",
            language="en"
        )
        
        # Call the API function
        from backend.api.openai_integration import analyze_rehabilitation_data
        response = await analyze_rehabilitation_data(request)
        
        # Verify the response
        self.assertEqual(response.response, "This is a mock AI response with some recommendations.\n- First recommendation\n- Second recommendation")
        self.assertEqual(response.recommendations, ["First recommendation", "Second recommendation"])
        
        # Verify OpenAI was called with correct parameters
        mock_openai_create.assert_called_once()
        args, kwargs = mock_openai_create.call_args
        self.assertEqual(kwargs["model"], "gpt-4o")
        self.assertGreaterEqual(len(kwargs["messages"]), 2)  # At least system and user message
        
    @patch('backend.api.openai_integration.openai.ChatCompletion.create')
    async def test_chat_completion(self, mock_openai_create):
        # Set up mock response
        mock_openai_create.return_value = self.mock_openai_response
        
        # Test request
        request = ChatCompletionRequest(
            messages=[{"role": "user", "content": "How can I improve my arm mobility?"}],
            language="en"
        )
        
        # Call the API function
        from backend.api.openai_integration import chat_completion
        response = await chat_completion(request)
        
        # Verify the response
        self.assertEqual(response.response, "This is a mock AI response with some recommendations.\n- First recommendation\n- Second recommendation")
        
        # Verify OpenAI was called with correct parameters
        mock_openai_create.assert_called_once()
        args, kwargs = mock_openai_create.call_args
        self.assertEqual(kwargs["model"], "gpt-4o")
        
    def test_get_system_prompt(self):
        # Test English prompts
        en_prompt = get_system_prompt("nihss", "en")
        self.assertIn("NIHSS score measures stroke severity", en_prompt)
        
        # Test Russian prompts
        ru_prompt = get_system_prompt("phq9", "ru")
        self.assertIn("PHQ-9", ru_prompt)
        self.assertIn("депрессии", ru_prompt)
        
        # Test with unsupported language (should default to English)
        default_prompt = get_system_prompt("movement", "fr")
        self.assertIn("movement assessment", default_prompt)

if __name__ == '__main__':
    unittest.main()
