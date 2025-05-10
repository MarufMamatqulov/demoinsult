
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.main import app
from backend.api.movement_assessment import analyze_movement, get_level, generate_ai_recommendations

client = TestClient(app)

class TestMovementAPI(unittest.TestCase):
    def test_get_level(self):
        self.assertEqual(get_level(15, 15), "Excellent")
        self.assertEqual(get_level(12, 15), "Good")
        self.assertEqual(get_level(9, 15), "Fair")
        self.assertEqual(get_level(6, 15), "Poor")
    
    @patch('backend.api.movement_assessment.openai.Completion.create')
    def test_generate_ai_recommendations(self, mock_openai):
        # Setup mock
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text="Test recommendation")]
        mock_openai.return_value = mock_response
        
        # Test
        result = generate_ai_recommendations(
            upper_limb_score=10, 
            lower_limb_score=9, 
            balance_score=8,
            total_score=27,
            upper_limb_level="Good", 
            lower_limb_level="Good", 
            balance_level="Good",
            overall_level="Good",
            language="en", 
            patient_age=65
        )
        
        # Assert
        self.assertEqual(result, "Test recommendation")
        mock_openai.assert_called_once()
        
    @patch('backend.api.movement_assessment.generate_ai_recommendations')
    def test_analyze_movement_endpoint(self, mock_recommendations):
        # Setup mock
        mock_recommendations.return_value = "Test AI recommendation"
        
        # Test data
        test_data = {
            "questions": [
                {"id": 1, "score": 3},
                {"id": 2, "score": 2},
                {"id": 3, "score": 3},
                {"id": 4, "score": 2},
                {"id": 5, "score": 3},
                {"id": 6, "score": 3},
                {"id": 7, "score": 2},
                {"id": 8, "score": 3},
                {"id": 9, "score": 2},
                {"id": 10, "score": 3},
                {"id": 11, "score": 2},
                {"id": 12, "score": 3},
                {"id": 13, "score": 2}
            ],
            "language": "en",
            "patient_name": "Test Patient",
            "patient_age": 65,
            "assessor_relationship": "Child"
        }
        
        # Call API
        response = client.post("/assessment/movement", json=test_data)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["upper_limb_score"], 13)
        self.assertEqual(data["lower_limb_score"], 10)
        self.assertEqual(data["balance_score"], 10)
        self.assertEqual(data["total_score"], 33)
        self.assertEqual(data["recommendations"], "Test AI recommendation")

if __name__ == "__main__":
    unittest.main()
