# tests/conftest.py

import pytest
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            hashed_password = generate_password_hash('testpassword')
            user = User(username='testuser', password=hashed_password)
            db.session.add(user)
            db.session.commit()
            yield client
            db.drop_all()


@pytest.fixture
def login(client):
    def do_login():
        return client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })

    return do_login
