import unittest
import json
import os
from unittest.mock import patch, MagicMock
from BackEndIncidencias.update_incidence.app import lambda_handler  # Ajusta el import según la ubicación del archivo
import mysql.connector

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

    @patch('BackEndIncidencias.update_incidence.app.mysql.connector.connect')
    def test_lambda_handler_update_success(self, mock_connect):
        # Configura el mock para la conexión a la base de datos
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Evento simulado con datos de actualización
        event = {
            'body': json.dumps({
                'titulo': 'Nuevo Título',
                'fecha': '2024-08-11',
                'descripcion': 'Nueva Descripción',
                'estatus': 2,
                'reporte_id': '1'
            })
        }
        context = {}

        # Llamar a la función Lambda
        response = lambda_handler(event, context)

        # Verificar la respuesta
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), 'Reporte actualizado correctamente')

    @patch('BackEndIncidencias.update_incidence.app.mysql.connector.connect')
    def test_lambda_handler_update_report_not_found(self, mock_connect):
        # Configura el mock para la conexión a la base de datos
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Evento simulado con datos de actualización
        event = {
            'body': json.dumps({
                'titulo': 'Título Inexistente',
                'fecha': '2024-08-11',
                'descripcion': 'Descripción Inexistente',
                'estatus': 3,
                'reporte_id': '999'
            })
        }
        context = {}

        # Llamar a la función Lambda
        response = lambda_handler(event, context)

        # Verificar la respuesta
        self.assertEqual(response['statusCode'], 404)
        self.assertEqual(json.loads(response['body']), 'Reporte no encontrado')

    @patch('BackEndIncidencias.update_incidence.app.mysql.connector.connect')
    def test_lambda_handler_missing_parameter(self, mock_connect):
        # Configura el mock para la conexión a la base de datos
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Evento simulado con falta de parámetros
        event = {
            'body': json.dumps({
                'titulo': 'Título Sin Fecha',
                'descripcion': 'Descripción Sin Fecha',
                'estatus': 2
                # Falta 'fecha' y 'reporte_id'
            })
        }
        context = {}

        # Llamar a la función Lambda
        response = lambda_handler(event, context)

        # Verificar la respuesta
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Bad request. Missing required parameter', json.loads(response['body']))

    @patch('BackEndIncidencias.update_incidence.app.mysql.connector.connect')
    def test_lambda_handler_database_error(self, mock_connect):
        # Configura el mock para simular un error en la base de datos
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = mysql.connector.Error('Test DB Error')
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Evento simulado que causa un error en la base de datos
        event = {
            'body': json.dumps({
                'titulo': 'Título de Error',
                'fecha': '2024-08-11',
                'descripcion': 'Descripción de Error',
                'estatus': 2,
                'reporte_id': '1'
            })
        }
        context = {}

        # Llamar a la función Lambda
        response = lambda_handler(event, context)

        # Verificar la respuesta
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Database error', json.loads(response['body']))

    @patch('BackEndIncidencias.update_incidence.app.mysql.connector.connect')
    def test_lambda_handler_generic_error(self, mock_connect):
        # Configura el mock para simular un error genérico
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception('Test Generic Error')
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Evento simulado que causa un error genérico
        event = {
            'body': json.dumps({
                'titulo': 'Título de Error Genérico',
                'fecha': '2024-08-11',
                'descripcion': 'Descripción de Error Genérico',
                'estatus': 2,
                'reporte_id': '1'
            })
        }
        context = {}

        # Llamar a la función Lambda
        response = lambda_handler(event, context)

        # Verificar la respuesta
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error', json.loads(response['body']))

if __name__ == '__main__':
    unittest.main()
