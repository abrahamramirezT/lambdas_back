import json
import unittest
from datetime import date
from unittest.mock import patch, MagicMock
from read_admin.app import lambda_handler

mock_succes = {
            "pathParameters": {
                "id": 1
            }
        }

class TestAppReadOne:



        @patch('app.mysql.connector.connect')
        def test_lambda_handler_success(self, mock_connect):
            # Mock para la conexión y cursor
            mock_cursor = MagicMock()
            mock_connect.return_value.cursor.return_value = mock_cursor

            # Mock para el evento
            mock_event = {
                'pathParameters': {'reporte_id': '1'}
            }

            # Mock para el resultado de la consulta
            mock_admin = (1, date(2023, 6, 1), 'Descripción de prueba', 'En progreso')
            mock_cursor.fetchone.return_value = mock_admin

            # Ejecutar la función lambda_handler con el evento mockeado
            response = lambda_handler(mock_event, None)

            # Verificar el resultado esperado
            expected_date_str = mock_admin[1].strftime('%Y-%m-%d')
            expected_body = {
                'statusCode': 200,
                'body': json.dumps({
                    'reporte_id': mock_admin[0],
                    'fecha': expected_date_str,
                    'descripcion': mock_admin[2],
                    'status': mock_admin[3],
                })
            }
            self.assertEqual(response, expected_body)

        @patch('app.mysql.connector.connect')
        def test_lambda_handler_reporte_no_encontrado(self, mock_connect):
            # Mock para la conexión y cursor
            mock_cursor = MagicMock()
            mock_connect.return_value.cursor.return_value = mock_cursor

            # Mock para el evento
            mock_event = {
                'pathParameters': {'reporte_id': '2'}  # Reporte ID que no existe
            }

            # Mock para el resultado de la consulta (ningún resultado encontrado)
            mock_cursor.fetchone.return_value = None

            # Ejecutar la función lambda_handler con el evento mockeado
            response = lambda_handler(mock_event, None)

            # Verificar el resultado esperado
            expected_body = {
                'statusCode': 404,
                'body': json.dumps({'error': 'Reporte no encontrado'})
            }
            self.assertEqual(response, expected_body)

        @patch('app.mysql.connector.connect')
        def test_lambda_handler_error_bd(self, mock_connect):
            # Mock para el error de conexión a la base de datos
            mock_connect.side_effect = Exception('Error de conexión')

            # Mock para el evento
            mock_event = {
                'pathParameters': {'reporte_id': '1'}
            }

            # Ejecutar la función lambda_handler con el evento mockeado
            response = lambda_handler(mock_event, None)

            # Verificar el resultado esperado
            expected_body = {
                'statusCode': 500,
                'body': json.dumps({'error': 'Error de conexión a la base de datos: Error de conexión'})
            }
            self.assertEqual(response, expected_body)

        def test_lambda_handler_key_error(self):
            # Mock para el evento sin 'pathParameters'
            mock_event = {}

            # Ejecutar la función lambda_handler con el evento mockeado
            response = lambda_handler(mock_event, None)

            # Verificar el resultado esperado
            expected_body = {
                'statusCode': 400,
                'body': json.dumps({'error': 'Falta la clave esperada en el evento: pathParameters'})
            }


