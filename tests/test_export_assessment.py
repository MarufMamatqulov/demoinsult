import unittest
import os
import shutil
from fastapi.testclient import TestClient
from backend.main import app
from datetime import datetime

class TestExportAssessment(unittest.TestCase):
    """Test cases for assessment export functionality"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.client = TestClient(app)
        
        # Create test exports directory if it doesn't exist
        self.test_export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_exports")
        os.makedirs(self.test_export_dir, exist_ok=True)
        
        # Test data for speech and hearing assessment
        self.speech_hearing_data = {
            "patient_name": "Test Patient",
            "patient_age": 65,
            "assessor_relationship": "Relative",
            "assessment_type": "speech_hearing",
            "language": "en",
            "assessment_data": {
                "speech_score": 10,
                "hearing_score": 12,
                "total_score": 22,
                "speech_level": "Good",
                "hearing_level": "Excellent",
                "overall_level": "Good",
                "recommendations": "This is a test recommendation for speech and hearing."
            }
        }
        
        # Test data for movement assessment
        self.movement_data = {
            "patient_name": "Test Patient",
            "patient_age": 65,
            "assessor_relationship": "Relative",
            "assessment_type": "movement",
            "language": "en",
            "assessment_data": {
                "upper_limb_score": 10,
                "lower_limb_score": 8,
                "balance_score": 9,
                "total_score": 27,
                "upper_limb_level": "Good",
                "lower_limb_level": "Good",
                "balance_level": "Excellent",
                "overall_level": "Good",
                "recommendations": "This is a test recommendation for movement."
            }
        }
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_export_dir):
            shutil.rmtree(self.test_export_dir)
    
    def test_export_speech_hearing_assessment(self):
        """Test exporting speech and hearing assessment to PDF"""
        response = self.client.post("/assessment/export", json=self.speech_hearing_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result["success"])
        self.assertTrue("file_path" in result)
        self.assertTrue(result["file_path"].endswith(".pdf"))
        
        # Check if a message is returned
        self.assertTrue("message" in result)
        self.assertTrue(len(result["message"]) > 0)
    
    def test_export_movement_assessment(self):
        """Test exporting movement assessment to PDF"""
        response = self.client.post("/assessment/export", json=self.movement_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result["success"])
        self.assertTrue("file_path" in result)
        self.assertTrue(result["file_path"].endswith(".pdf"))
        
        # Check if a message is returned
        self.assertTrue("message" in result)
        self.assertTrue(len(result["message"]) > 0)
    
    def test_export_invalid_assessment_type(self):
        """Test exporting with invalid assessment type"""
        invalid_data = self.speech_hearing_data.copy()
        invalid_data["assessment_type"] = "invalid_type"
        
        response = self.client.post("/assessment/export", json=invalid_data)
        self.assertEqual(response.status_code, 200)  # API still returns 200 but with failure info
        result = response.json()
        self.assertFalse(result["success"])
        self.assertEqual(result["file_path"], "")
        self.assertTrue("Invalid assessment type" in result["message"])
    
    def test_multilanguage_support(self):
        """Test exporting assessments in different languages"""
        # Test Spanish
        spanish_data = self.speech_hearing_data.copy()
        spanish_data["language"] = "es"
        
        response = self.client.post("/assessment/export", json=spanish_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result["success"])
        
        # Test Russian
        russian_data = self.speech_hearing_data.copy()
        russian_data["language"] = "ru"
        
        response = self.client.post("/assessment/export", json=russian_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result["success"])

if __name__ == "__main__":
    unittest.main()
