import unittest
from unittest.mock import patch
from flask import session
from app import app  # Replace with the actual name of your Flask app module

class DashboardTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_db_connection')  # Mock the database connection
    def test_dashboard_access(self, mock_get_db_connection):
        # Mock session to simulate a logged-in user
        with self.app.session_transaction() as sess:
            sess['user_id'] = 'test_user'

        # Mock the database response
        mock_conn = mock_get_db_connection.return_value
        mock_conn.execute.return_value.fetchone.return_value = {
            'user_id': 'test_user',
            'name': 'Test User',
            'age': 30,
            'gender': 'M',
            'gender_preference': 'F',
            'location': 'New York',
            'interests': 'music,sports'
        }

        # Access the dashboard page
        response = self.app.get('/dashboard')

        # Check that the page loads correctly
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)
        self.assertIn(b'30', response.data)
        self.assertIn(b'New York', response.data)

if __name__ == '__main__':
    unittest.main()
