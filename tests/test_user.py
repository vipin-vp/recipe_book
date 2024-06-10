# tests/test_user.py
from app.models import User
from test_conftest import client, login


def test_register(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpassword'
    })
    assert response.status_code == 302  # Redirect to login page
    user = User.query.filter_by(username='newuser').first()
    assert user is not None


def test_login(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302  # Redirect to index page
    assert b'Invalid username or password' not in response.data


def test_logout(client, login):
    login()
    response = client.get('/logout')
    assert response.status_code == 302  # Redirect to index page
