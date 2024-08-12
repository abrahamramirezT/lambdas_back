import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from botocore.exceptions import ClientError
import json
import os

from read_all_incidence.app import lambda_handler, get_secret


class TestReadAllInstancesLambdaFunction(unittest.TestCase):

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('read_all_incidence.app.boto3.session.Session.client')
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
    @patch('read_all_incidence.app.get_secret')
    @patch('read_all_incidence.app.mysql.connector.connect')
    def test_lambda_handler_success(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (1, 'Titulo 1', '2024-08-11', 'Descripcion 1', 'Estatus 1', 'url1'),
            (2, 'Titulo 2', '2024-08-12', 'Descripcion 2', 'Estatus 2', 'url2')
        ]

        event = {}

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(len(json.loads(response['body'])), 2)

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('read_all_incidence.app.get_secret')
    @patch('read_all_incidence.app.mysql.connector.connect')
    def test_lambda_handler_no_reports(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = []  # Simula que no se encuentran reportes

        event = {}

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 404)
        self.assertIn('No se encontraron reportes', json.loads(response['body'])['error'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('read_all_incidence.app.get_secret')
    @patch('read_all_incidence.app.mysql.connector.connect')
    def test_lambda_handler_db_error(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        mock_connect.side_effect = mysql.connector.Error('Database connection failed')  # Simula un error en la conexión

        event = {}

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error de base de datos', json.loads(response['body'])['error'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('read_all_incidence.app.get_secret')
    @patch('read_all_incidence.app.mysql.connector.connect')
    def test_lambda_handler_key_error(self, mock_connect, mock_get_secret):
        mock_get_secret.side_effect = KeyError('MY_SECRET_NAME')  # Simula una KeyError en la obtención del secreto

        event = {}

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Clave faltante en el evento', json.loads(response['body'])['error'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('read_all_incidence.app.get_secret')
    @patch('read_all_incidence.app.mysql.connector.connect')
    def test_lambda_handler_unexpected_error(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        mock_connect.side_effect = Exception('Unexpected error')  # Simula un error inesperado

        event = {}

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error inesperado', json.loads(response['body'])['error'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('read_all_incidence.app.boto3.session.Session.client')
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
