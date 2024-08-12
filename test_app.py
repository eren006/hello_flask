import pytest
from app import app, get_db_connection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Set up the database for testing
            conn = get_db_connection()
            conn.execute('DROP TABLE IF EXISTS user_profiles')
            conn.execute('''
                CREATE TABLE user_profiles (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    gender_preference TEXT NOT NULL,
                    location TEXT NOT NULL,
                    interests TEXT NOT NULL
                )
            ''')
            conn.execute('''
                INSERT INTO user_profiles (user_id, name, age, gender, gender_preference, location, interests)
                VALUES ('testuser', 'Test User', 25, 'male', 'female', 'Test City', 'Reading,Traveling')
            ''')
            conn.commit()
            conn.close()
        yield client

def test_login_redirect_to_dashboard(client):
    # Simulate logging in with the correct credentials
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'Test User'
    }, follow_redirects=True)

    # Check that the login was successful and the user is redirected to the dashboard
    assert response.status_code == 200
    assert b'Your Profile' in response.data
    assert b'Test User' in response.data
    assert b'Test City' in response.data
