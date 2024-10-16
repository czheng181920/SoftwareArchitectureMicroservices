import unittest
import json
from app import app  # Assuming your Flask app is in app.py

class TestMeetingsIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test client using the Flask application configured for testing
        cls.app = app.test_client()
        cls.app.testing = True

    def test_query_all_meetings(self):
        # Make a GET request to the /meetings endpoint
        response = self.app.get('/meetings')
        
        # Verify the status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the response is in JSON format
        self.assertEqual(response.content_type, 'application/json')

        # Further assertions can be made to check the content of the response
        data = response.get_json()
        print("Data Layer Response:", response.text)
        self.assertIsInstance(data, list)  # Assuming the response is a list of meetings
        # Additional checks can be added based on the expected structure of the meeting data

if __name__ == '__main__':
    unittest.main()
