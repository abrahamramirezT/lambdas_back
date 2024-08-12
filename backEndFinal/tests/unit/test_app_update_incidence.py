import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from botocore.exceptions import ClientError
import json
import os
import base64

from update_incidence.app import lambda_handler, get_secret


class TestUpdateIncidenceLambdaFunction(unittest.TestCase):

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1', 'S3_BUCKET': 'test_bucket'})
    @patch('update_incidence.app.boto3.session.Session.client')
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

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1', 'S3_BUCKET': 'test_bucket'})
    @patch('update_incidence.app.get_secret')
    @patch('update_incidence.app.mysql.connector.connect')
    @patch('update_incidence.app.s3_client.put_object')
    def test_lambda_handler_success_with_image(self, mock_put_object, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.rowcount = 1

        event = {
            'body': json.dumps({
                'titulo': 'Reporte Test',
                'fecha': '2024-08-11',
                'descripcion': 'Descripción del reporte',
                'estatus': 'Abierto',
                'reporte_id': 1,
                'fto_base64': base64.b64encode(b"dummy_image_data").decode('utf-8')
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Reporte actualizado correctamente', response['body'])
        mock_put_object.assert_called_once()

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1', 'S3_BUCKET': 'test_bucket'})
    @patch('update_incidence.app.get_secret')
    @patch('update_incidence.app.mysql.connector.connect')
    def test_lambda_handler_success_without_image(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.rowcount = 1

        event = {
            'body': json.dumps({
                'titulo': 'Reporte Test',
                'fecha': '2024-08-11',
                'descripcion': 'Descripción del reporte',
                'estatus': 'Abierto',
                'reporte_id': 1
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Reporte actualizado correctamente', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1', 'S3_BUCKET': 'test_bucket'})
    @patch('update_incidence.app.get_secret')
    @patch('update_incidence.app.mysql.connector.connect')
    def test_lambda_handler_report_not_found(self, mock_connect, mock_get_secret):
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
            'body': json.dumps({
                'titulo': 'Reporte Test',
                'fecha': '2024-08-11',
                'descripcion': 'Descripción del reporte',
                'estatus': 'Abierto',
                'reporte_id': 1
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 404)
        self.assertIn('Reporte no encontrado', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1', 'S3_BUCKET': 'test_bucket'})
    @patch('update_incidence.app.get_secret')
    @patch('update_incidence.app.mysql.connector.connect')
    def test_lambda_handler_key_error(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        event = {
            'body': json.dumps({
                'titulo': 'Reporte Test',
                'descripcion': 'Descripción del reporte',
                'estatus': 'Abierto',
                'reporte_id': 1
            })  # Falta la clave 'fecha'
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Bad request. Missing required parameter', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1', 'S3_BUCKET': 'test_bucket'})
    @patch('update_incidence.app.get_secret')
    @patch('update_incidence.app.mysql.connector.connect')
    def test_lambda_handler_db_error(self, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        mock_connect.side_effect = mysql.connector.Error('Database connection failed')

        event = {
            'body': json.dumps({
                'titulo': 'Reporte Test',
                'fecha': '2024-08-11',
                'descripcion': 'Descripción del reporte',
                'estatus': 'Abierto',
                'reporte_id': 1
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Database error', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1', 'S3_BUCKET': 'test_bucket'})
    @patch('update_incidence.app.get_secret')
    @patch('update_incidence.app.mysql.connector.connect')
    @patch('update_incidence.app.s3_client.put_object')
    def test_lambda_handler_image_processing_error(self, mock_put_object, mock_connect, mock_get_secret):
        mock_get_secret.return_value = {
            'host': 'test_host',
            'username': 'test_user',
            'password': 'test_password',
            'dbname': 'test_db'
        }

        mock_put_object.side_effect = Exception('Error al procesar la imagen')

        event = {
            'body': json.dumps({
                'titulo': 'Reporte Test',
                'fecha': '2024-08-11',
                'descripcion': 'Descripción del reporte',
                'estatus': 'Abierto',
                'reporte_id': 1,
                'fto_base64': base64.b64encode(b"dummy_image_data").decode('utf-8')
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Error al procesar la imagen', response['body'])

    @patch.dict(os.environ, {'MY_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1', 'S3_BUCKET': 'test_bucket'})
    @patch('update_incidence.app.boto3.session.Session.client')
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
