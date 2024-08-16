import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from mysql.connector import Error
from create_incidence.app import lambda_handler, get_secret
import os
import json
import base64

class TestCreateIncidenceLambda(unittest.TestCase):

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('create_incidence.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    @patch('create_incidence.app.s3_client.put_object')
    def test_lambda_handler_success(self, mock_s3_put, mock_connect, mock_boto_client):
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
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Evento simulado con datos válidos
        event = {
            "body": json.dumps({
                "titulo": "Incidencia de prueba",
                "fecha": "2023-08-20",
                "descripcion": "Descripción de la incidencia",
                "estudiante": "Estudiante 1",
                "aula": 101,
                "edificio": 1,
                "matricula": "MAT123",
                "grado": 10,
                "grupo": 2,
                "div_academica": 1,
                "estatus": "Pendiente",
                "fto_base64": base64.b64encode(b'Test image data').decode('utf-8')
            })
        }

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Incidencia creada exitosamente', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('create_incidence.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    def test_lambda_handler_missing_params(self, mock_connect, mock_boto_client):
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

        # Evento simulado con datos faltantes
        event = {
            "body": json.dumps({
                "titulo": "Incidencia de prueba",
                "fecha": "2023-08-20"
                # Faltan otros campos requeridos
            })
        }

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Solicitud incorrecta. Faltan parámetros requeridos.', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('create_incidence.app.boto3.session.Session.client')
    @patch('mysql.connector.connect')
    @patch('create_incidence.app.s3_client.put_object')
    def test_lambda_handler_s3_error(self, mock_s3_put, mock_connect, mock_boto_client):
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

        # Simulación de un error al subir a S3
        mock_s3_put.side_effect = Exception("Error al subir la imagen a S3")

        # Evento simulado con datos válidos
        event = {
            "body": json.dumps({
                "titulo": "Incidencia de prueba",
                "fecha": "2023-08-20",
                "descripcion": "Descripción de la incidencia",
                "estudiante": "Estudiante 1",
                "aula": 101,
                "edificio": 1,
                "matricula": "MAT123",
                "grado": 10,
                "grupo": 2,
                "div_academica": 1,
                "estatus": "Pendiente",
                "fto_base64": base64.b64encode(b'Test image data').decode('utf-8')
            })
        }

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error al subir la imagen a S3', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('create_incidence.app.boto3.session.Session.client')
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

        # Evento simulado con datos válidos
        event = {
            "body": json.dumps({
                "titulo": "Incidencia de prueba",
                "fecha": "2023-08-20",
                "descripcion": "Descripción de la incidencia",
                "estudiante": "Estudiante 1",
                "aula": 101,
                "edificio": 1,
                "matricula": "MAT123",
                "grado": 10,
                "grupo": 2,
                "div_academica": 1,
                "estatus": "Pendiente",
                "fto_base64": base64.b64encode(b'Test image data').decode('utf-8')
            })
        }

        response = lambda_handler(event, None)

        # Validaciones
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error de base de datos', response['body'])

    @patch.dict(os.environ, {
        'MY_SECRET_NAME': 'test_secret',
        'MY_AWS_REGION': 'us-west-2',
        'S3_BUCKET': 'test-bucket'
    })
    @patch('create_incidence.app.boto3.session.Session.client')
    def test_get_secret_client_error(self, mock_boto_client):
        # Simulación de un error al obtener el secreto
        mock_secrets_client = MagicMock()
        mock_secrets_client.get_secret_value.side_effect = Exception("Failed to retrieve secret")
        mock_boto_client.return_value = mock_secrets_client

        with self.assertRaises(Exception):
            get_secret('invalid_secret_name', 'us-west-2')


if __name__ == '__main__':
    unittest.main()
