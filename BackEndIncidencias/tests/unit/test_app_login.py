import unittest
import json
import boto3
from botocore.exceptions import ClientError
from BackEndIncidencias.login.app import lambda_handler  # Ajusta el import según la ubicación del archivo


class TestLambdaHandler(unittest.TestCase):

    def setUp(self):
        # Configura las variables necesarias antes de cada prueba
        self.client = boto3.client('cognito-idp', region_name='us-east-1')
        self.client_id = "1sbarp1jth6oiihie71719sgk5"
        self.user_pool_id = 'us-east-1_6Upf2mMUO'

    def test_lambda_handler_success(self):
        # Crea un evento simulado para una autenticación exitosa
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': 'testpassword'
            })
        }
        context = {}

        # Realiza la llamada a la función Lambda
        response = lambda_handler(event, context)

        # Verifica que el código de estado sea 200
        self.assertEqual(response['statusCode'], 200)

        # Verifica que la respuesta contenga los tokens y rol
        response_body = json.loads(response['body'])
        self.assertIn('id_token', response_body)
        self.assertIn('access_token', response_body)
        self.assertIn('refresh_token', response_body)
        self.assertIn('role', response_body)

    def test_lambda_handler_client_error(self):
        # Configura el cliente para lanzar un ClientError
        self.client = boto3.client('cognito-idp', region_name='us-east-1')
        self.client.exceptions.ClientError = ClientError
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': 'testpassword'
            })
        }
        context = {}

        # Reemplaza el cliente de Cognito con uno que simula un error
        with self.assertRaises(ClientError):
            response = lambda_handler(event, context)

        # Verifica que el código de estado sea 400
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('error_message', json.loads(response['body']))

    def test_lambda_handler_generic_error(self):
        # Configura el cliente para lanzar una excepción genérica
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': 'testpassword'
            })
        }
        context = {}

        # Manipula el cliente para lanzar una excepción genérica
        with self.assertRaises(Exception):
            response = lambda_handler(event, context)

        # Verifica que el código de estado sea 500
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error_message', json.loads(response['body']))

    def test_lambda_handler_missing_parameters(self):
        # Crea un evento simulado con parámetros faltantes
        event = {
            'body': json.dumps({
                'username': 'testuser'
                # Falta 'password'
            })
        }
        context = {}

        # Realiza la llamada a la función Lambda
        response = lambda_handler(event, context)

        # Verifica que el código de estado sea 500
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error_message', json.loads(response['body']))


if __name__ == '__main__':
    unittest.main()
