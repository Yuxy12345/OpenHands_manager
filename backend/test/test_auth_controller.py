import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from flask_jwt_extended import JWTManager
from src.controller.auth_controller import auth_bp

class TestAuthController(unittest.TestCase):
    def setUp(self):
        # Set up Flask app and register blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(auth_bp)
        self.app.config['JWT_SECRET_KEY'] = 'test_secret'
        self.jwt = JWTManager(self.app)
        self.client = self.app.test_client()

    @patch('controller.auth_controller.userDao')
    def test_register_success(self, mock_userDao):
        # Mock userDao behavior
        mock_userDao.get_by_username.return_value = None
        mock_userDao.create_user = MagicMock()

        # Test data
        data = {"username": "testuser", "password": "testpassword"}

        # Make POST request
        response = self.client.post('/api/register', data=json.dumps(data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "注册成功"})
        mock_userDao.create_user.assert_called_once()

    @patch('controller.auth_controller.userDao')
    def test_register_existing_user(self, mock_userDao):
        # Mock userDao behavior
        mock_userDao.get_by_username.return_value = MagicMock()

        # Test data
        data = {"username": "testuser", "password": "testpassword"}

        # Make POST request
        response = self.client.post('/api/register', data=json.dumps(data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "用户名已存在"})

    def test_register_missing_fields(self):
        # Test data
        data = {"username": ""}

        # Make POST request
        response = self.client.post('/api/register', data=json.dumps(data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "需要提供用户名和密码"})

    @patch('controller.auth_controller.User')
    def test_login_success(self, mock_user):
        # Mock User behavior
        mock_user.query.filter_by.return_value.first.return_value = MagicMock(
            id=1, password="hashedpassword"
        )
        with patch('controller.auth_controller.check_password_hash', return_value=True):
            # Test data
            data = {"username": "testuser", "password": "testpassword"}

            # Make POST request
            response = self.client.post('/api/login', data=json.dumps(data), content_type='application/json')

            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)

    @patch('controller.auth_controller.User')
    def test_login_user_not_found(self, mock_user):
        # Mock User behavior
        mock_user.query.filter_by.return_value.first.return_value = None

        # Test data
        data = {"username": "testuser", "password": "testpassword"}

        # Make POST request
        response = self.client.post('/api/login', data=json.dumps(data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "用户不存在"})

    @patch('controller.auth_controller.User')
    def test_login_wrong_password(self, mock_user):
        # Mock User behavior
        mock_user.query.filter_by.return_value.first.return_value = MagicMock(
            id=1, password="hashedpassword"
        )
        with patch('controller.auth_controller.check_password_hash', return_value=False):
            # Test data
            data = {"username": "testuser", "password": "wrongpassword"}

            # Make POST request
            response = self.client.post('/api/login', data=json.dumps(data), content_type='application/json')

            # Assertions
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json, {"error": "密码错误"})

if __name__ == '__main__':
    unittest.main()