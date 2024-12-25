import unittest
from flask import Flask
from flask_testing import TestCase
import create_app, db
from models import User, userResult

class TestFlaskApp(TestCase):

    def create_app(self):
        # Set up the app for testing with the test config
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
        app.config['SECRET_KEY'] = 'testsecret'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # Create the database and tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop the database tables after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        # Test the registration of a new user
        response = self.client.post('/register', data={
            'fullname': 'maneliforoutan',
            'username': 'maneli',
            'email': 'maneli0foroutan@gmail.com',
            'password': '123456',
            'confirm_password': '123456'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertIn(b'Registration successful!', response.data)

        # Check if the user was added to the database
        user = User.query.filter_by(username='maneli').first()
        self.assertIsNotNone(user)

    # def test_login_user(self):
    #     # First register a user
    #     self.client.post('/register', data={
    #         'fullname': 'maneliforoutan',
    #         'username': 'maneli',
    #         'email': 'maneli0foroutan@gmail.com',
    #         'password': 'm-123456',
    #         'confirm_password': 'm-123456'
    #     })
        
    #     # Test login with valid credentials
    #     response = self.client.post('/login', data={
    #         'username': 'maneli',
    #         'password': 'm-123456'
    #     })
    #     self.assertEqual(response.status_code, 302)  # Redirect to profile page
    #     self.assertIn(b'Login successful!', response.data)

    #     # Test login with invalid credentials
    #     response = self.client.post('/login', data={
    #         'username': 'maneli',
    #         'password': 'wrongpassword'
    #     })
    #     self.assertEqual(response.status_code, 200)  # Stay on login page
    #     self.assertIn(b'Invalid username or password.', response.data)

    # def test_result_submission(self):
    #     # First register and login a user
    #     self.client.post('/register', data={
    #         'fullname': 'maneliforoutan',
    #         'username': 'maneli',
    #         'email': 'maneli0foroutan@gmail.com',
    #         'password': 'm-123456',
    #         'confirm_password': 'm-123456'
    #     })
    #     self.client.post('/login', data={
    #         'username': 'maneli',
    #         'password': 'm-123456'
    #     })
        
    #     # Test result submission
    #     response = self.client.post('/result', data={
    #         'color': 'G',
    #         'cut': 'Ideal',
    #         'clarity': 'VS1',
    #         'carat': 1.23,
    #         'depth': 61.5,
    #         'table': 57.0,
    #         'x': 5.7,
    #         'y': 5.7,
    #         'z': 3.2
    #     })
    #     self.assertEqual(response.status_code, 302)  # Redirect to profile page after submission
    #     self.assertIn(b'Result saved!', response.data)

    #     # Check if the result is stored in the database
    #     result = userResult.query.filter_by(user_id=1).first()  # Assuming the user ID is 1
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.color, 'G')

if __name__ == '__main__':
    unittest.main()
