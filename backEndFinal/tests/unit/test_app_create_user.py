import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from botocore.exceptions import ClientError
import json
import os

from create_user.app import lambda_handler, get_secret


class TestCreateUserLambdaHandler(unittest.TestCase):

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('create_user.app.boto3.session.Session.client')
    def test_get_secret(self, mock_boto_client):
        mock_client = mock_boto_client.return_value
        mock_client.get_secret_value.return_value = {
            'SecretString': json.dumps({
                'host': 'test_host',
                'username': 'test_user',
                'password': 'test_password',
                'dbname': 'test_db'
            })
        }

        secret_name = os.environ['MY_SECRET_NAME']
        region_name = os.environ['MY_AWS_REGION']
        secret = get_secret(secret_name, region_name)
        self.assertEqual(secret['host'], 'test_host')
        self.assertEqual(secret['username'], 'test_user')
        self.assertEqual(secret['password'], 'test_password')
        self.assertEqual(secret['dbname'], 'test_db')

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('create_user.app.get_secret')
    @patch('create_user.app.mysql.connector.connect')
    def test_lambda_handler_success(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value

        event = {
            "body": json.dumps({
                "username": "test_user",
                "password": "securepassword"
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('User creado exitosamente', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('create_user.app.get_secret')
    @patch('create_user.app.mysql.connector.connect')
    def test_lambda_handler_invalid_json(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        event = {
            "body": "Invalid JSON String"
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Solicitud incorrecta. El cuerpo debe ser un JSON válido.', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('create_user.app.get_secret')
    @patch('create_user.app.mysql.connector.connect')
    def test_lambda_handler_missing_fields(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        event = {
            "body": json.dumps({
                "username": "test_user"
                # Falta el campo "password"
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Solicitud incorrecta. Faltan parámetros requeridos.', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('create_user.app.get_secret')
    @patch('create_user.app.mysql.connector.connect')
    def test_lambda_handler_db_error(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }
        mock_connect.side_effect = mysql.connector.Error('Database connection failed')

        event = {
            "body": json.dumps({
                "username": "test_user",
                "password": "securepassword"
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error de base de datos', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('create_user.app.get_secret')
    @patch('create_user.app.mysql.connector.connect')
    def test_lambda_handler_empty_fields(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        event = {
            "body": json.dumps({
                "username": "",
                "password": ""
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Solicitud incorrecta. Faltan parámetros requeridos.', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('create_user.app.boto3.session.Session.client')
    def test_get_secret_client_error(self, mock_boto_client):
        mock_client = mock_boto_client.return_value
        mock_client.get_secret_value.side_effect = ClientError(
            {'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
            'GetSecretValue'
        )

        with self.assertRaises(ClientError):
            get_secret('invalid_secret', 'us-east-1')


if __name__ == '__main__':
    unittest.main()
