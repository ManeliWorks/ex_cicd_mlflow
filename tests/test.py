import pytest
from flask import url_for
from app import app, db, User  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    app.config['WTF_CSRF_ENABLED'] = False 

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all() 

def test_register_user(client):
    response = client.post(url_for('register'), data={
        'fullname': 'Test User',
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'securepassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Successfully registered! Please log in." in response.data

    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.email == 'testuser@example.com'

def test_register_duplicate_username(client):
    client.post(url_for('register'), data={
        'fullname': 'User One',
        'username': 'duplicateuser',
        'email': 'userone@example.com',
        'password': 'password1'
    }, follow_redirects=True)

    response = client.post(url_for('register'), data={
        'fullname': 'User Two',
        'username': 'duplicateuser',
        'email': 'usertwo@example.com',
        'password': 'password2'
    }, follow_redirects=True)

    assert b"Username already taken, please choose a different one." in response.data

def test_login_user(client):
    client.post(url_for('register'), data={
        'fullname': 'Test User',
        'username': 'testlogin',
        'email': 'testlogin@example.com',
        'password': 'securepassword'
    }, follow_redirects=True)

    response = client.post(url_for('login'), data={
        'username': 'testlogin',
        'password': 'securepassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Login successful!" in response.data

def test_login_invalid_user(client):
    response = client.post(url_for('login'), data={
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert b"Invalid username or password" in response.data

def test_logout_user(client):
    client.post(url_for('register'), data={
        'fullname': 'Test User',
        'username': 'testlogout',
        'email': 'testlogout@example.com',
        'password': 'securepassword'
    }, follow_redirects=True)

    client.post(url_for('login'), data={
        'username': 'testlogout',
        'password': 'securepassword'
    }, follow_redirects=True)

    response = client.get(url_for('logout'), follow_redirects=True)

    assert response.status_code == 200
    assert b"You have been logged out successfully." in response.data
