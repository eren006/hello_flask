import unittest
from flask import session
from app import app, db_manager
from unittest.mock import MagicMock

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        print("TESTING FUNCTION: setUp")
        # Set up the test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True
        
        # Mock the database manager methods
        self.mock_db = MagicMock()
        db_manager.fetch_one = self.mock_db.fetch_one
        db_manager.fetch_all = self.mock_db.fetch_all
        db_manager.execute_query = self.mock_db.execute_query

    # Test for the home route (should redirect to login)
    def test_home_route(self):
        print("TESTING FUNCTION: test_home_route")
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirection
        self.assertIn('/login', response.location)

    # Test for the login route (GET)
    def test_login_get(self):
        print("TESTING FUNCTION: test_login_get")
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    # Test for login form submission (POST) with valid credentials
    def test_login_post_valid(self):
        print("TESTING FUNCTION: test_login_post_valid")
        # Mock valid credentials in the database
        db_manager.fetch_one.return_value = ('23', 'male', 'Calgary', 'test', 'test', 'Dancing,Drawing,Exercising,smoking,drinking', '123456', 'male', 'english,french,mandarin')
        
        form_data = {
        'username': 'test',  # Form field name is 'username'
        'password': '123456'  # Form field name is 'password'
        }
        
        response = self.app.post('/login', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    # Test for login form submission (POST) with invalid credentials
    def test_login_post_invalid(self):
        print("TESTING FUNCTION: test_login_post_invalid")
        self.mock_db.fetch_one.return_value = None
        
        response = self.app.post('/login', data={'username': 'wrong', 'password': 'wrong'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Test for profile creation (GET)
    def test_create_get(self):
        print("TESTING FUNCTION: test_create_get")
        response = self.app.get('/create')
        self.assertEqual(response.status_code, 200)

    # Test for profile creation (POST)
    def test_create_post(self):
        print("TESTING FUNCTION: test_create_post")
        form_data={
            'user_id': 'user',
            'password': 'password',
            'name': 'Test User',
            'age': '25',
            'gender': 'male',
            'gender_preference': 'female',
            'province':'Ontario',
            'city': 'Toronto',
            'smoking': 'false',
            'drinking': 'false',
            'languages': ['English'],
            'interests': ['Coding', 'Music']
        }
        response = self.app.post('/create', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Test for profile editing (GET)
    # def test_edit_profile_get(self):
    #     print("TESTING FUNCTION: test_edit_profile_get")
    #     with self.app.session_transaction() as sess:
    #         sess['user_id'] = 'user_id'
        
    #     self.mock_db.fetch_one.return_value = ('user', 'password', 'name', 25, 'user_id', 'male', 'city', 'female', 'languages')
        
    #     response = self.app.get('/edit_profile')
    #     self.assertEqual(response.status_code, 200)
    
    
    # def test_delete_user(self):
    #     print("TESTING FUNCTION: test_delete_user")
    #     # Simulate a logged-in user by setting the session
    #     with self.app.session_transaction() as sess:
    #         sess['user_id'] = 'user_id'
    
    #     # Mock the database query for deleting user records
    #     self.mock_db.execute_query = MagicMock()

    #     # Simulate the deletion request
    #     response = self.app.post('/delete', follow_redirects=True)

    #     # Verify that the appropriate SQL queries were executed for deleting    the user
    #     self.mock_db.execute_query.assert_any_call(query="DELETE FROM records   WHERE userA = ? OR userB = ?", params=('user_id', 'user_id'))
    #     self.mock_db.execute_query.assert_any_call(query="DELETE FROM User  WHERE UserID = ?", params=('user_id',))

    #     # Check that the session has been cleared
    #     with self.app.session_transaction() as sess:
    #         self.assertIsNone(sess.get('user_id'))

    #     # Verify the user is redirected to the login page
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Login', response.data)  # Assuming the word 'Login'     is in the template



    # Additional tests for like, dislike, and delete routes can be added similarly

if __name__ == '__main__':
    unittest.main()
