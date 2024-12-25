import unittest
from flask import Flask
from flask_testing import TestCase
from Flask_APP import create_app, db
from Flask_APP.database_models import User, userResult

class TestFlaskApp(TestCase):

    def create_app(self):
        app = create_app()
        app.config['WTF_CSRF_ENABLED'] = False 
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
        app.config['SECRET_KEY'] = 'testsecret'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        response = self.client.get('/register')


        response = self.client.post('/register', data={
            'fullname': 'maneliforoutan',
            'username': 'mnl',
            'email': 'maneli0foroutan@gmail.com',
            'password': '123456',
            'confirm_password': '123456',

        })

        self.assertEqual(response.status_code, 302)
        user = User.query.filter_by(username='mnl').first()
        self.assertIsNotNone(user)

    # def test_register_user_password_mismatch(self):
    #     response = self.client.post('/register', data={
    #         'fullname': 'maneliforoutan',
    #         'username': 'mnl',
    #         'email': 'maneli0foroutan@gmail.com',
    #         'password': '123456',
    #         'confirm_password': 'wrongpassword',  # Mismatched password
    #     })
        
    #     self.assertEqual(response.status_code, 200) 
    #     self.assertIn(b'Passwords must match', response.data)  

    def test_login_user(self):
        self.client.post('/register', data={
            'fullname': 'maneliforoutan',
            'username': 'mnl',
            'email': 'maneli0foroutan@gmail.com',
            'password': '123456',
        })

        response = self.client.post('/login', data={
            'username': 'maneli',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200) 
        self.assertIn(b'Invalid username or password.', response.data)


        
    def test_result_submission(self):
        self.client.post('/register', data={
            'fullname': 'maneli foroutan',
            'username': 'mnl',
            'email': 'maneli0foroutan@gmail.com',
            'password': '123456',
        })
        
        self.client.post('/login', data={
            'username': 'mnl',
            'password': '123456'
        })
        
        response = self.client.post('/result', data={
            'carat': [0.23],  
            'cut': ['Ideal'], 
            'color': ['E'],  
            'clarity': ['SI2'], 
            'depth': [61.5], 
            'table': [55],  
            'x': [3.95],  
            'y': [3.98],  
            'z': [2.43]  
        })
        
        self.assertEqual(response.status_code, 302) 

        response = self.client.get('/profile')
        
        self.assertIn(b'Profile', response.data)  
        
        result = userResult.query.filter_by(user_id=1).first()
        
        self.assertIsNotNone(result)
        
        self.assertEqual(result.color, 'E')

if __name__ == '__main__':
    unittest.main()




