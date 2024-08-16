import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from mysql.connector import Error
from update_incidence.app import lambda_handler, get_secret
import os
import json
import base64

class TestUpdateIncidenceLambda(unittest.TestCase):

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('update_incidence.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    @patch('update_incidence.app.s3_client.put_object')
    def test_lambda_handler_success_with_image(self, mock_s3_put, mock_connect, mock_boto_client):
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

        # Simulación de la conexión y ejecución exitosa en la base de datos
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1  # Simular que se ha actualizado un registro
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Evento simulado con imagen
        event = {
            "body": json.dumps({
                "id": 1,
                "estatus": "Completado",
                "fto_base64": base64.b64encode(b'Test image data').decode('utf-8')
            })
        }

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Reporte actualizado correctamente', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('update_incidence.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    def test_lambda_handler_success_without_image(self, mock_connect, mock_boto_client):
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

        # Simulación de la conexión y ejecución exitosa en la base de datos
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1  # Simular que se ha actualizado un registro
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Evento simulado sin imagen
        event = {
            "body": json.dumps({
                "id": 1,
                "estatus": "Completado"
            })
        }

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Reporte actualizado correctamente', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('update_incidence.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    def test_lambda_handler_report_not_found(self, mock_connect, mock_boto_client):
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

        # Simulación de la conexión y que no se encuentre el registro
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0  # Simular que no se ha actualizado ningún registro
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Evento simulado
        event = {
            "body": json.dumps({
                "id": 99,
                "estatus": "Completado"
            })
        }

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 404)
        self.assertIn('Reporte no encontrado', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('update_incidence.app.boto3.session.Session.client')
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
        mock_connect.side_effect = Error("Error de conexión a la base de datos")

        # Evento simulado
        event = {
            "body": json.dumps({
                "id": 1,
                "estatus": "Completado"
            })
        }

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Database error', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('update_incidence.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    def test_lambda_handler_missing_parameter(self, mock_connect, mock_boto_client):
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

        # Evento simulado con un parámetro faltante
        event = {
            "body": json.dumps({
                "estatus": "Completado"
            })
        }

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Bad request. Missing required parameter', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('update_incidence.app.boto3.session.Session.client')
    def test_get_secret_client_error(self, mock_boto_client):
        # Simulación de un error al obtener el secreto
        mock_secrets_client = MagicMock()
        mock_secrets_client.get_secret_value.side_effect = Exception("Failed to retrieve secret")
        mock_boto_client.return_value = mock_secrets_client

        with self.assertRaises(Exception):
            get_secret('invalid_secret_name', 'us-west-2')


if __name__ == '__main__':
    unittest.main()
