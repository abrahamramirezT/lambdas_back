import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from botocore.exceptions import ClientError
import json
import os

from delete_incidence.app import lambda_handler, get_secret


class TestLambdaFunction(unittest.TestCase):

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('delete_incidence.app.boto3.session.Session.client')
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
    @patch('delete_incidence.app.get_secret')
    @patch('delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_success(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.rowcount = 1  # Simula que se encontró y eliminó el reporte

        event = {
            'pathParameters': {'reporte_id': '1'}
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], json.dumps('Incidencia borrada exitosamente'))

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('delete_incidence.app.get_secret')
    @patch('delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_not_found(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.rowcount = 0  # Simula que no se encontró el reporte

        event = {
            'pathParameters': {'reporte_id': '1'}
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 404)
        self.assertEqual(response['body'], json.dumps('Reporte no encontrado'))

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('delete_incidence.app.get_secret')
    @patch('delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_db_error(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }
        mock_connect.side_effect = mysql.connector.Error('Database connection failed')  # Simula un error en la conexión

        event = {
            'pathParameters': {'reporte_id': '1'}
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Database error', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('delete_incidence.app.get_secret')
    @patch('delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_key_error(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        event = {}  # Simula que no se proporciona `pathParameters`

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Bad request. Missing required parameter', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('delete_incidence.app.boto3.session.Session.client')
    def test_get_secret_client_error(self, mock_boto_client):
        mock_client = mock_boto_client.return_value
        mock_client.get_secret_value.side_effect = ClientError(
            {'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
            'GetSecretValue'
        )

        with self.assertRaises(ClientError):
            get_secret('invalid_secret', 'us-east-1')

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('delete_incidence.app.get_secret')
    @patch('delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_no_reporte_id(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        event = {
            'pathParameters': {}  # Simula que no se proporciona `reporte_id`
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Bad request. Missing required parameter', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('delete_incidence.app.get_secret')
    @patch('delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_invalid_reporte_id(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        event = {
            'pathParameters': {'reporte_id': 'invalid'}  # Simula un `reporte_id` inválido
        }

        with self.assertRaises(ValueError):  # Suponiendo que el código lanza un ValueError
            lambda_handler(event, None)


if __name__ == '__main__':
    unittest.main()