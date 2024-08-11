import json
import unittest
from unittest.mock import patch
from botocore.exceptions import ClientError
from BackEndIncidencias.set_password.app import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    @patch('boto3.client')
    def test_successful_password_change(self, mock_boto_client):
        # Configura el cliente simulado
        mock_cognito_client = mock_boto_client.return_value
        mock_cognito_client.admin_initiate_auth.return_value = {
            'ChallengeName': 'NEW_PASSWORD_REQUIRED',
            'Session': 'mock_session'
        }
        mock_cognito_client.respond_to_auth_challenge.return_value = {}

        # Define el evento de prueba
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'temporary_password': 'tempPass123!',
                'new_password': 'newPass123!'
            })
        }

        # Llama a la función Lambda
        response = lambda_handler(event, None)

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), {"message": "Password changed successfully."})

    @patch('boto3.client')
    def test_temporary_password_not_set(self, mock_boto_client):
        # Configura el cliente simulado para no establecer la contraseña temporal
        mock_cognito_client = mock_boto_client.return_value
        mock_cognito_client.admin_initiate_auth.return_value = {
            'ChallengeName': 'NEW_PASSWORD_REQUIRED',
            'Session': 'mock_session'
        }
        mock_cognito_client.respond_to_auth_challenge.side_effect = ClientError(
            {"Error": {"Message": "Temporary password not set"}}, "RespondToAuthChallenge"
        )

        # Define el evento de prueba
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'temporary_password': 'tempPass123!',
                'new_password': 'newPass123!'
            })
        }

        # Llama a la función Lambda
        response = lambda_handler(event, None)

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(json.loads(response['body']), {"error_message": "Temporary password not set"})

    @patch('boto3.client')
    def test_authentication_error(self, mock_boto_client):
        # Configura el cliente simulado para lanzar un error en la autenticación
        mock_cognito_client = mock_boto_client.return_value
        mock_cognito_client.admin_initiate_auth.side_effect = ClientError(
            {"Error": {"Message": "Authentication error"}}, "AdminInitiateAuth"
        )

        # Define el evento de prueba
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'temporary_password': 'tempPass123!',
                'new_password': 'newPass123!'
            })
        }

        # Llama a la función Lambda
        response = lambda_handler(event, None)

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(json.loads(response['body']), {"error_message": "Authentication error"})

    @patch('boto3.client')
    def test_missing_parameters(self, mock_boto_client):
        # Configura el cliente simulado
        mock_cognito_client = mock_boto_client.return_value
        mock_cognito_client.admin_initiate_auth.return_value = {
            'ChallengeName': 'NEW_PASSWORD_REQUIRED',
            'Session': 'mock_session'
        }
        mock_cognito_client.respond_to_auth_challenge.return_value = {}

        # Define el evento de prueba con parámetros faltantes
        event = {
            'body': json.dumps({
                'username': 'testuser',
                # Falta 'temporary_password' y 'new_password'
            })
        }

        # Llama a la función Lambda
        response = lambda_handler(event, None)

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(json.loads(response['body']), {"error_message": "Missing parameters"})

    @patch('boto3.client')
    def test_unexpected_exception(self, mock_boto_client):
        # Configura el cliente simulado para lanzar una excepción inesperada
        mock_cognito_client = mock_boto_client.return_value
        mock_cognito_client.admin_initiate_auth.side_effect = Exception("Unexpected error")

        # Define el evento de prueba
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'temporary_password': 'tempPass123!',
                'new_password': 'newPass123!'
            })
        }

        # Llama a la función Lambda
        response = lambda_handler(event, None)

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(json.loads(response['body']), {"error_message": "Unexpected error"})

if __name__ == '__main__':
    unittest.main()
