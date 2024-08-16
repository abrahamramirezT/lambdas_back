import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from mysql.connector import Error
from read_grupo_all.app import lambda_handler, get_secret
import os
import json

class TestReadGrupoAllLambda(unittest.TestCase):

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2'
    })
    @patch('read_grupo_all.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    def test_lambda_handler_success(self, mock_connect, mock_boto_client):
        # Simulación de la respuesta de Secrets Manager
        mock_secrets_client = MagicMock()
        mock_secrets_client.get_secret_value.return_value = {
            'SecretString': json.dumps({
                'host': 'localhost',
                'username': 'user',
                'password': 'password',
                'dbname': 'test_db'
            })
        }
        mock_boto_client.return_value = mock_secrets_client

        # Simulación de la conexión y consulta exitosa a la base de datos
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, 'Grupo 1'), (2, 'Grupo 2')]
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Evento simulado
        event = {}

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Grupo 1', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2'
    })
    @patch('read_grupo_all.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    def test_lambda_handler_no_groups_found(self, mock_connect, mock_boto_client):
        # Simulación de la respuesta de Secrets Manager
        mock_secrets_client = MagicMock()
        mock_secrets_client.get_secret_value.return_value = {
            'SecretString': json.dumps({
                'host': 'localhost',
                'username': 'user',
                'password': 'password',
                'dbname': 'test_db'
            })
        }
        mock_boto_client.return_value = mock_secrets_client

        # Simulación de la conexión y consulta vacía en la base de datos
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Evento simulado
        event = {}

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 404)
        self.assertIn('No se encontraron reportes', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2'
    })
    @patch('read_grupo_all.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    def test_lambda_handler_db_error(self, mock_connect, mock_boto_client):
        # Simulación de la respuesta de Secrets Manager
        mock_secrets_client = MagicMock()
        mock_secrets_client.get_secret_value.return_value = {
            'SecretString': json.dumps({
                'host': 'localhost',
                'username': 'user',
                'password': 'password',
                'dbname': 'test_db'
            })
        }
        mock_boto_client.return_value = mock_secrets_client

        # Simulación de un error de conexión a la base de datos
        mock_connect.side_effect = Error("Error de conexión")

        # Evento simulado
        event = {}

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error de base de datos', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2'
    })
    @patch('read_grupo_all.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    def test_lambda_handler_key_error(self, mock_connect, mock_boto_client):
        # Simulación de la respuesta de Secrets Manager
        mock_boto_client.side_effect = KeyError("MY_SECRET_NAME")

        # Evento simulado
        event = {}

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Clave faltante en el evento', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2'
    })
    @patch('read_grupo_all.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    def test_lambda_handler_unexpected_error(self, mock_connect, mock_boto_client):
        # Simulación de la respuesta de Secrets Manager
        mock_secrets_client = MagicMock()
        mock_secrets_client.get_secret_value.return_value = {
            'SecretString': json.dumps({
                'host': 'localhost',
                'username': 'user',
                'password': 'password',
                'dbname': 'test_db'
            })
        }
        mock_boto_client.return_value = mock_secrets_client

        # Simulación de un error inesperado
        mock_connect.side_effect = Exception("Unexpected error")

        # Evento simulado
        event = {}

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error inesperado', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2'
    })
    @patch('read_grupo_all.app.boto3.session.Session.client')
    def test_get_secret_client_error(self, mock_boto_client):
        # Simulación de un error al obtener el secreto
        mock_secrets_client = MagicMock()
        mock_secrets_client.get_secret_value.side_effect = Exception("Failed to retrieve secret")
        mock_boto_client.return_value = mock_secrets_client

        with self.assertRaises(Exception):
            get_secret('invalid_secret_name', 'us-west-2')


if __name__ == '__main__':
    unittest.main()
