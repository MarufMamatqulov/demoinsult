import unittest
from fastapi.testclient import TestClient
from backend.main import app

class TestPatientChat(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        
        # Test data
        self.chat_request = {
            "messages": [
                {"role": "user", "content": "How can I help my father recover from stroke?"}
            ],
            "language": "en"
        }
        
        self.assessment_advice_request = {
            "assessment_type": "speech_hearing",
            "results": {
                "speech_score": 12,
                "hearing_score": 10,
                "total_score": 22,
                "speech_level": "Good",
                "hearing_level": "Fair",
                "overall_level": "Good",
            },
            "language": "en"
        }
    
    def test_patient_chat_endpoint(self):
        """Test the patient chat API endpoint"""
        response = self.client.post("/chat/patient-chat", json=self.chat_request)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("response", data)
        self.assertTrue(len(data["response"]) > 0)
    
    def test_multilingual_support(self):
        """Test that the chat API supports multiple languages"""
        # Test Russian
        russian_request = self.chat_request.copy()
        russian_request["language"] = "ru"
        
        response = self.client.post("/chat/patient-chat", json=russian_request)
        self.assertEqual(response.status_code, 200)
        
        # Test Spanish
        spanish_request = self.chat_request.copy()
        spanish_request["language"] = "es"
        
        response = self.client.post("/chat/patient-chat", json=spanish_request)
        self.assertEqual(response.status_code, 200)
    
    def test_assessment_advice_endpoint(self):
        """Test the assessment advice API endpoint"""
        response = self.client.post("/chat/assessment-advice", json=self.assessment_advice_request)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("advice", data)
        self.assertTrue(data["advice"] is not None)
        self.assertTrue(len(data["advice"]) > 0)
    
    def test_assessment_advice_different_types(self):
        """Test the assessment advice API with different assessment types"""
        # Test movement assessment
        movement_request = self.assessment_advice_request.copy()
        movement_request["assessment_type"] = "movement"
        movement_request["results"] = {
            "upper_limb_score": 10,
            "lower_limb_score": 8,
            "balance_score": 9,
            "total_score": 27,
            "upper_limb_level": "Good",
            "lower_limb_level": "Good",
            "balance_level": "Good",
            "overall_level": "Good",
        }
        
        response = self.client.post("/chat/assessment-advice", json=movement_request)
        self.assertEqual(response.status_code, 200)
        
        # Test PHQ-9 assessment
        phq9_request = self.assessment_advice_request.copy()
        phq9_request["assessment_type"] = "phq9"
        phq9_request["results"] = {
            "score": 8,
            "category": "Mild depression"
        }
        
        response = self.client.post("/chat/assessment-advice", json=phq9_request)
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_assessment_type(self):
        """Test with an invalid assessment type"""
        invalid_request = self.assessment_advice_request.copy()
        invalid_request["assessment_type"] = "invalid_type"
        
        response = self.client.post("/chat/assessment-advice", json=invalid_request)
        self.assertEqual(response.status_code, 200)  # The API still returns 200 with generic advice
    
    def test_missing_required_fields(self):
        """Test with missing required fields"""
        # Missing assessment type
        incomplete_request = {
            "results": self.assessment_advice_request["results"],
            "language": "en"
        }
        
        response = self.client.post("/chat/assessment-advice", json=incomplete_request)
        self.assertEqual(response.status_code, 400)  # Should return 400 Bad Request

if __name__ == "__main__":
    unittest.main()
