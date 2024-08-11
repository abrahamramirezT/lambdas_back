import unittest
import json
import os
from datetime import datetime
from BackEndIncidencias.read_all_incidence.app import lambda_handler  # Asegúrate de que la ruta sea correcta
from mysql.connector import Error
from unittest.mock import patch

# Mock classes for different test scenarios
class MockConnectionSuccess:
    def cursor(self):
        return MockCursorSuccess()

    def close(self):
        pass

class MockCursorSuccess:
    def execute(self, sql):
        pass

    def fetchall(self):
        return [
            (1, 'Reporte 1', datetime(2024, 8, 10), 'Descripción 1', 'Estatus 1', 'url1'),
            (2, 'Reporte 2', datetime(2024, 8, 11), 'Descripción 2', 'Estatus 2', 'url2')
        ]

    def close(self):
        pass

class MockConnectionQueryError:
    def cursor(self):
        return MockCursorQueryError()

    def close(self):
        pass

class MockCursorQueryError:
    def execute(self, sql):
        pass

    def fetchall(self):
        raise Error("Error en la consulta")

    def close(self):
        pass

class MockConnectionConnectError:
    def cursor(self):
        raise Error("Error en la conexión")

    def close(self):
        pass

class MockConnectionUnexpectedError:
    def cursor(self):
        return MockCursorUnexpectedError()

    def close(self):
        pass

class MockCursorUnexpectedError:
    def execute(self, sql):
        pass

    def fetchall(self):
        raise Exception("Error inesperado")

    def close(self):
        pass

class TestLambdaHandler(unittest.TestCase):
    def setUp(self):
        # Guardar las variables de entorno originales
        self.original_env = dict(os.environ)

    def tearDown(self):
        # Restaurar las variables de entorno originales
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_successful_fetch(self):
        # Define las variables de entorno necesarias
        os.environ['RDS_HOST'] = 'mock_host'
        os.environ['RDS_USER'] = 'mock_user'
        os.environ['RDS_PASSWORD'] = 'mock_password'
        os.environ['RDS_DB'] = 'mock_db'

        # Llama a la función Lambda usando el conector simulado para éxito
        with patch('mysql.connector.connect', return_value=MockConnectionSuccess()):
            response = lambda_handler({}, {})

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 200)
        expected_body = json.dumps([
            {'reporte_id': 1, 'titulo': 'Reporte 1', 'fecha': '2024-08-10', 'descripcion': 'Descripción 1', 'estatus': 'Estatus 1', 'fto_url': 'url1'},
            {'reporte_id': 2, 'titulo': 'Reporte 2', 'fecha': '2024-08-11', 'descripcion': 'Descripción 2', 'estatus': 'Estatus 2', 'fto_url': 'url2'}
        ])
        self.assertEqual(response['body'], expected_body)

    def test_query_error(self):
        # Define las variables de entorno necesarias
        os.environ['RDS_HOST'] = 'mock_host'
        os.environ['RDS_USER'] = 'mock_user'
        os.environ['RDS_PASSWORD'] = 'mock_password'
        os.environ['RDS_DB'] = 'mock_db'

        # Llama a la función Lambda usando el conector simulado para error en la consulta
        with patch('mysql.connector.connect', return_value=MockConnectionQueryError()):
            response = lambda_handler({}, {})

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(json.loads(response['body']), {'error': 'Error de base de datos'})

    def test_connection_error(self):
        # Define las variables de entorno necesarias
        os.environ['RDS_HOST'] = 'mock_host'
        os.environ['RDS_USER'] = 'mock_user'
        os.environ['RDS_PASSWORD'] = 'mock_password'
        os.environ['RDS_DB'] = 'mock_db'

        # Llama a la función Lambda usando el conector simulado para error en la conexión
        with patch('mysql.connector.connect', side_effect=Error("Error en la conexión")):
            response = lambda_handler({}, {})

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(json.loads(response['body']), {'error': 'Error de base de datos'})

    def test_unexpected_error(self):
        # Define las variables de entorno necesarias
        os.environ['RDS_HOST'] = 'mock_host'
        os.environ['RDS_USER'] = 'mock_user'
        os.environ['RDS_PASSWORD'] = 'mock_password'
        os.environ['RDS_DB'] = 'mock_db'

        # Llama a la función Lambda usando el conector simulado para error inesperado
        with patch('mysql.connector.connect', return_value=MockConnectionUnexpectedError()):
            response = lambda_handler({}, {})

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(json.loads(response['body']), {'error': 'Error inesperado', 'message': 'Error inesperado'})

if __name__ == '__main__':
    unittest.main()
