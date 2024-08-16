import unittest
from unittest.mock import patch, MagicMock
import boto3
from botocore.exceptions import ClientError
import json
import os

from login.app import lambda_handler, get_secret


class TestLoginLambdaFunction(unittest.TestCase):

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('login.app.boto3.session.Session.client')
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
    @patch('login.app.get_secret')
    @patch('login.app.boto3.client')
    def test_lambda_handler_success(self, mock_boto_client, mock_get_secret):
        mock_get_secret.return_value = {
            'client_id': 'test_client_id',
            'user_pool_id': 'test_user_pool_id'
        }

        mock_client = mock_boto_client.return_value
        mock_client.initiate_auth.return_value = {
            'AuthenticationResult': {
                'IdToken': 'test_id_token',
                'AccessToken': 'test_access_token',
                'RefreshToken': 'test_refresh_token'
            }
        }
        mock_client.admin_list_groups_for_user.return_value = {
            'Groups': [{'GroupName': 'test_role'}]
        }

        event = {
            'body': json.dumps({
                'username': 'test_user',
                'password': 'test_password'
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('id_token', json.loads(response['body']))
        self.assertIn('access_token', json.loads(response['body']))
        self.assertIn('refresh_token', json.loads(response['body']))
        self.assertEqual(json.loads(response['body'])['role'], 'test_role')

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('login.app.get_secret')
    @patch('login.app.boto3.client')
    def test_lambda_handler_invalid_credentials(self, mock_boto_client, mock_get_secret):
        mock_get_secret.return_value = {
            'client_id': 'test_client_id',
            'user_pool_id': 'test_user_pool_id'
        }

        mock_client = mock_boto_client.return_value
        mock_client.initiate_auth.side_effect = ClientError(
            {'Error': {'Message': 'Incorrect username or password.'}},
            'InitiateAuth'
        )

        event = {
            'body': json.dumps({
                'username': 'invalid_user',
                'password': 'invalid_password'
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('error_message', json.loads(response['body']))
        self.assertEqual(json.loads(response['body'])['error_message'], 'Incorrect username or password.')

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('login.app.get_secret')
    @patch('login.app.boto3.client')
    def test_lambda_handler_missing_parameters(self, mock_boto_client, mock_get_secret):
        mock_get_secret.return_value = {
            'client_id': 'test_client_id',
            'user_pool_id': 'test_user_pool_id'
        }

        event = {
            'body': json.dumps({})  # Missing username and password
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error_message', json.loads(response['body']))

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('login.app.boto3.session.Session.client')
    def test_get_secret_client_error(self, mock_boto_client):
        mock_client = mock_boto_client.return_value
        mock_client.get_secret_value.side_effect = ClientError(
            {'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
            'GetSecretValue'
        )

        with self.assertRaises(ClientError):
            get_secret('invalid_secret', 'us-east-1')

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('login.app.get_secret')
    @patch('login.app.boto3.client')
    def test_lambda_handler_user_not_found(self, mock_boto_client, mock_get_secret):
        mock_get_secret.return_value = {
            'client_id': 'test_client_id',
            'user_pool_id': 'test_user_pool_id'
        }

        mock_client = mock_boto_client.return_value
        mock_client.initiate_auth.return_value = {
            'AuthenticationResult': {
                'IdToken': 'test_id_token',
                'AccessToken': 'test_access_token',
                'RefreshToken': 'test_refresh_token'
            }
        }
        mock_client.admin_list_groups_for_user.side_effect = ClientError(
            {'Error': {'Code': 'UserNotFoundException', 'Message': 'User does not exist.'}},
            'AdminListGroupsForUser'
        )

        event = {
            'body': json.dumps({
                'username': 'test_user',
                'password': 'test_password'
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('error_message', json.loads(response['body']))
        self.assertEqual(json.loads(response['body'])['error_message'], 'User does not exist.')

    @patch.dict(os.environ, {'MY_COGNITO_SECRET_NAME': 'test_secret', 'MY_AWS_REGION': 'us-east-1'})
    @patch('login.app.get_secret')
    @patch('login.app.boto3.client')
    def test_lambda_handler_unknown_error(self, mock_boto_client, mock_get_secret):
        mock_get_secret.return_value = {
            'client_id': 'test_client_id',
            'user_pool_id': 'test_user_pool_id'
        }

        mock_client = mock_boto_client.return_value
        mock_client.initiate_auth.side_effect = Exception('Unknown error')

        event = {
            'body': json.dumps({
                'username': 'test_user',
                'password': 'test_password'
            })
        }

        response = lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error_message', json.loads(response['body']))
        self.assertEqual(json.loads(response['body'])['error_message'], 'Unknown error')


if __name__ == '__main__':
    unittest.main()
