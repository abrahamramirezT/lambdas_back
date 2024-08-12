import unittest
from unittest.mock import patch, MagicMock
import boto3
from botocore.exceptions import ClientError
import json
import os

from set_password.app import lambda_handler, get_secret


class TestSetPasswordLambdaFunction(unittest.TestCase):

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('set_password.app.boto3.session.Session.client')
    def test_get_secret(self, mock_boto_client):
        mock_client = mock_boto_client.return_value
        mock_client.get_secret_value.return_value = {
            'SecretString': json.dumps({
                'client_id': 'test_client_id',
                'user_pool_id': 'test_user_pool_id'
            })
        }

        secret_name = os.environ['MY_COGNITO_SECRET_NAME']
        region_name = os.environ['MY_AWS_REGION']
        secret = get_secret(secret_name, region_name)
        self.assertEqual(secret['client_id'], 'test_client_id')
        self.assertEqual(secret['user_pool_id'], 'test_user_pool_id')

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('set_password.app.get_secret')
    @patch('set_password.app.boto3.client')
    def test_lambda_handler_success(self, mock_boto_client, mock_get_secret):
        mock_get_secret.return_value = {
            'client_id': 'test_client_id',
            'user_pool_id': 'test_user_pool_id'
        }

        mock_client = mock_boto_client.return_value
        mock_client.admin_initiate_auth.return_value = {
            'ChallengeName': 'NEW_PASSWORD_REQUIRED',
            'Session': 'test_session'
        }

        event = {
            'body': json.dumps({
                'username': 'test_user',
                'temporary_password': 'temp_pass',
                'new_password': 'new_pass'
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Contraseña cambiada exitosamente', response['body'])

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('set_password.app.get_secret')
    @patch('set_password.app.boto3.client')
    def test_lambda_handler_no_password_change_required(self, mock_boto_client, mock_get_secret):
        mock_get_secret.return_value = {
            'client_id': 'test_client_id',
            'user_pool_id': 'test_user_pool_id'
        }

        mock_client = mock_boto_client.return_value
        mock_client.admin_initiate_auth.return_value = {
            'ChallengeName': 'OTHER_CHALLENGE'
        }

        event = {
            'body': json.dumps({
                'username': 'test_user',
                'temporary_password': 'temp_pass',
                'new_password': 'new_pass'
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('No se requiere cambiar la contraseña', response['body'])

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('set_password.app.get_secret')
    @patch('set_password.app.boto3.client')
    def test_lambda_handler_client_error(self, mock_boto_client, mock_get_secret):
        mock_get_secret.return_value = {
            'client_id': 'test_client_id',
            'user_pool_id': 'test_user_pool_id'
        }

        mock_client = mock_boto_client.return_value
        mock_client.admin_initiate_auth.side_effect = ClientError(
            {'Error': {'Message': 'Client error occurred'}},
            'AdminInitiateAuth'
        )

        event = {
            'body': json.dumps({
                'username': 'test_user',
                'temporary_password': 'temp_pass',
                'new_password': 'new_pass'
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error de cliente', response['body'])

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('set_password.app.get_secret')
    @patch('set_password.app.boto3.client')
    def test_lambda_handler_json_decode_error(self, mock_boto_client, mock_get_secret):
        mock_get_secret.return_value = {
            'client_id': 'test_client_id',
            'user_pool_id': 'test_user_pool_id'
        }

        event = {
            'body': '{invalid_json}'
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Error al decodificar JSON', response['body'])

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('set_password.app.get_secret')
    @patch('set_password.app.boto3.client')
    def test_lambda_handler_unexpected_error(self, mock_boto_client, mock_get_secret):
        mock_get_secret.return_value = {
            'client_id': 'test_client_id',
            'user_pool_id': 'test_user_pool_id'
        }

        mock_client = mock_boto_client.return_value
        mock_client.admin_initiate_auth.side_effect = Exception('Unexpected error occurred')

        event = {
            'body': json.dumps({
                'username': 'test_user',
                'temporary_password': 'temp_pass',
                'new_password': 'new_pass'
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error inesperado', response['body'])

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('set_password.app.boto3.session.Session.client')
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
