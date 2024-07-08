import json
import  unittest
from datetime import date
from unittest.mock import patch

import mysql

from read_one_incidence import app

class TestReadOne(unittest.TestCase):


    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    def test_lambda_handler(self):
        mock_body = {
            "pathParameters": {"reporte_id": "1"}
        }

        result = app.lambda_handler(mock_body, None)
        status_code = result['statusCode']
        self.assertEqual(status_code, 200)
        body = json.loads(result['body'])
        self.assertIn("reporte_id", body)
        self.assertIn("fecha", body)
        self.assertIn("descripcion", body)
        self.assertIn("status", body)



    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch("mysql.connector.connect")
    def test_lambda_handler_database_connection_error(self, mock_connect):
        # Configurar el mock para que lance una excepción al intentar conectarse
        mock_connect.side_effect = mysql.connector.Error("Error de conexión simulado")

        # Simular evento
        mock_event = {
            "pathParameters": {"reporte_id": "1"}
        }

        # Ejecutar función lambda_handler
        result = app.lambda_handler(mock_event, None)

        # Verificar el resultado esperado (500)
        self.assertEqual(result['statusCode'], 500)
        body = json.loads(result['body'])
        self.assertIn("error", body)
        self.assertIn("Error de conexión a la base de datos", body['error'])

    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch("mysql.connector.connect")
    def test_lambda_handler_reporte_not_found(self, mock_connect):
        # Crear mocks manualmente
        mock_connection = unittest.mock.Mock()
        mock_cursor = unittest.mock.Mock()

        # Configurar el comportamiento de los mocks
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        # Simular evento con un ID que no existe
        mock_event = {
            "pathParameters": {"reporte_id": "999"}
        }

        # Ejecutar función lambda_handler
        result = app.lambda_handler(mock_event, None)

        # Verificar el resultado esperado (404)
        self.assertEqual(result['statusCode'], 404)
        body = json.loads(result['body'])
        self.assertIn("error", body)
        self.assertEqual(body['error'], 'Reporte no encontrado')

    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch("mysql.connector.connect")
    def test_lambda_handler_bad_request(self, mock_connect):
        # Crear mocks manualmente
        mock_connection = unittest.mock.Mock()
        mock_cursor = unittest.mock.Mock()

        # Configurar el comportamiento de los mocks
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Simular evento sin la clave 'pathParameters'
        mock_event = {}  # Evento vacío para provocar KeyError

        # Ejecutar función lambda_handler
        result = app.lambda_handler(mock_event, None)

        # Verificar el resultado esperado (400)
        self.assertEqual(result['statusCode'], 400)
        body = json.loads(result['body'])
        self.assertIn("error", body)
        self.assertTrue(body['error'].startswith("Falta la clave esperada en el evento:"))

    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch("mysql.connector.connect")
    def test_lambda_handler_unexpected_error(self, mock_connect):
        # Crear mocks manualmente
        mock_connection = unittest.mock.Mock()
        mock_cursor = unittest.mock.Mock()

        # Configurar el mock de conexión para lanzar una excepción inesperada
        mock_connect.side_effect = Exception("Error inesperado de prueba")

        # Simular evento con un ID válido
        mock_event = {
            "pathParameters": {"reporte_id": "1"}
        }

        # Ejecutar función lambda_handler
        result = app.lambda_handler(mock_event, None)

        # Verificar el resultado esperado (500)
        self.assertEqual(result['statusCode'], 500)
        body = json.loads(result['body'])
        self.assertIn("error", body)
        self.assertEqual(body['error'], "Error inesperado: Error inesperado de prueba")

    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch("mysql.connector.connect")
    def test_lambda_handler_successful_data_processing(self, mock_connect):
        # Crear mocks
        mock_connection = unittest.mock.Mock()
        mock_cursor = unittest.mock.Mock()

        # Configurar el comportamiento de los mocks
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Simular un resultado de la base de datos
        mock_cursor.fetchone.return_value = (1, date(2023, 7, 1), "Descripción de prueba", "Activo")

        # Simular evento
        mock_event = {
            "pathParameters": {"reporte_id": "1"}
        }

        # Ejecutar función lambda_handler
        result = app.lambda_handler(mock_event, None)

        # Verificar el resultado esperado
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['reporte_id'], 1)
        self.assertEqual(body['fecha'], "2023-07-01")
        self.assertEqual(body['descripcion'], "Descripción de prueba")
        self.assertEqual(body['status'], "Activo")


    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch("mysql.connector.connect")
    def test_lambda_handler_different_database_errors(self, mock_connect):
        errors = [
            mysql.connector.errors.InterfaceError("Interface Error"),
            mysql.connector.errors.DatabaseError("Database Error"),
            mysql.connector.errors.ProgrammingError("Programming Error")
        ]

        for error in errors:
            mock_connect.side_effect = error

            mock_event = {
                "pathParameters": {"reporte_id": "1"}
            }

            result = app.lambda_handler(mock_event, None)

            self.assertEqual(result['statusCode'], 500)
            body = json.loads(result['body'])
            self.assertIn("error", body)
            self.assertIn("Error de conexión a la base de datos", body['error'])
            self.assertIn(str(error), body['error'])


    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch("mysql.connector.connect")
    def test_lambda_handler_different_id_types(self, mock_connect):
        # Crear mocks
        mock_connection = unittest.mock.Mock()
        mock_cursor = unittest.mock.Mock()

        # Configurar el comportamiento de los mocks
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # Simular que no se encuentra el reporte

        id_types = ["999999999999999999", "0", "-1", "abc", "!@#$%^&*()"]

        for id_type in id_types:
            mock_event = {
                "pathParameters": {"reporte_id": id_type}
            }

            result = app.lambda_handler(mock_event, None)

            self.assertEqual(result['statusCode'], 404)
            body = json.loads(result['body'])
            self.assertIn("error", body)
            self.assertEqual(body['error'], 'Reporte no encontrado')

if __name__ == '__main__':
    unittest.main()