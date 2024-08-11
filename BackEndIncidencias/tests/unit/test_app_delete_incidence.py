import unittest
import json
import os
from unittest.mock import patch
from BackEndIncidencias.delete_incidence.app import lambda_handler  # Ajusta el import según la ubicación del archivo


class TestLambdaHandler(unittest.TestCase):

    def setUp(self):
        # Configura las variables de entorno para la base de datos de prueba
        os.environ['RDS_HOST'] = 'host_de_pruebas'
        os.environ['RDS_USER'] = 'usuario_de_pruebas'
        os.environ['RDS_PASSWORD'] = 'contraseña_de_pruebas'
        os.environ['RDS_DB'] = 'db_de_pruebas'

    def tearDown(self):
        # Limpia las variables de entorno
        os.environ.pop('RDS_HOST', None)
        os.environ.pop('RDS_USER', None)
        os.environ.pop('RDS_PASSWORD', None)
        os.environ.pop('RDS_DB', None)

    @patch('BackEndIncidencias.delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_success(self, mock_connect):
        # Configura el mock para la conexión a la base de datos
        def mock_cursor():
            class Cursor:
                def __init__(self):
                    self.rowcount = 1

                def execute(self, sql, params):
                    pass

                def close(self):
                    pass

            return Cursor()

        mock_connect.return_value.cursor = mock_cursor

        # Evento simulado que coincide con los datos de la base de pruebas
        event = {'pathParameters': {'reporte_id': '1'}}
        context = {}

        # Llamar a la función Lambda
        response = lambda_handler(event, context)

        # Verificar la respuesta
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), 'Incidencia borrada exitosamente')

    @patch('BackEndIncidencias.delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_report_not_found(self, mock_connect):
        # Configura el mock para la conexión a la base de datos
        def mock_cursor():
            class Cursor:
                def __init__(self):
                    self.rowcount = 0

                def execute(self, sql, params):
                    pass

                def close(self):
                    pass

            return Cursor()

        mock_connect.return_value.cursor = mock_cursor

        # Evento simulado que no encuentra el reporte
        event = {'pathParameters': {'reporte_id': '2'}}
        context = {}

        # Llamar a la función Lambda
        response = lambda_handler(event, context)

        # Verificar la respuesta
        self.assertEqual(response['statusCode'], 404)
        self.assertEqual(json.loads(response['body']), 'Reporte no encontrado')

    @patch('BackEndIncidencias.delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_missing_path_parameter(self, mock_connect):
        # Configura el mock para la conexión a la base de datos
        def mock_cursor():
            class Cursor:
                def __init__(self):
                    self.rowcount = 0

                def execute(self, sql, params):
                    pass

                def close(self):
                    pass

            return Cursor()

        mock_connect.return_value.cursor = mock_cursor

        # Evento simulado con falta de parámetros
        event = {}
        context = {}

        # Llamar a la función Lambda
        response = lambda_handler(event, context)

        # Verificar la respuesta
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Bad request. Missing required parameter', json.loads(response['body']))

    @patch('BackEndIncidencias.delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_database_error(self, mock_connect):
        # Configura el mock para la conexión a la base de datos
        def mock_cursor():
            raise Exception('Test DB Error')

        mock_connect.return_value.cursor = mock_cursor

        # Evento simulado que causa un error en la base de datos
        event = {'pathParameters': {'reporte_id': '1'}}
        context = {}

        # Llamar a la función Lambda
        response = lambda_handler(event, context)

        # Verificar la respuesta
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Database error', json.loads(response['body']))

    @patch('BackEndIncidencias.delete_incidence.app.mysql.connector.connect')
    def test_lambda_handler_generic_error(self, mock_connect):
        # Configura el mock para la conexión a la base de datos
        def mock_cursor():
            raise Exception('Test Generic Error')

        mock_connect.return_value.cursor = mock_cursor

        # Evento simulado que causa un error genérico
        event = {'pathParameters': {'reporte_id': '1'}}
        context = {}

        # Llamar a la función Lambda
        response = lambda_handler(event, context)

        # Verificar la respuesta
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error', json.loads(response['body']))


if __name__ == '__main__':
    unittest.main()
