import json
import  unittest
from unittest.mock import patch
import mysql.connector
import mysql
from create_incidence import app


mock_body = {
            "body": json.dumps({
                "fecha": "2024-07-07",
                "descripcion": "Incidencia de prueba",
                "status": "abierto"
            })
        }


class TestCreateIncidence(unittest.TestCase):

    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch('mysql.connector.connect')
    def test_lambda_handler_insert(self, mock_connect):
        mock_connection = unittest.mock.Mock()
        mock_cursor = unittest.mock.Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        result = app.lambda_handler(mock_body, None)
        status_code = result['statusCode']
        self.assertEqual(status_code, 200)
        self.assertEqual(json.loads(result['body']), 'Incidencia creada exitosamente')



    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch('mysql.connector.connect')
    def test_lambda_handler_insert_error(self, mock_connect):
        mock_connection = unittest.mock.Mock()
        mock_cursor = unittest.mock.Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Simular un error al ejecutar el comando SQL
        mock_cursor.execute.side_effect = mysql.connector.Error("Error de inserción")

        mock_body = {
            "body": json.dumps({
                "fecha": "2024-07-07",
                "descripcion": "Incidencia de prueba",
                "status": "abierto"
            })
        }

        result = app.lambda_handler(mock_body, None)
        status_code = result['statusCode']
        self.assertEqual(status_code, 500)
        self.assertEqual(json.loads(result['body']), {'error': 'Error de base de datos'})

    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch('mysql.connector.connect')
    def test_lambda_handler_json_decode_error(self, mock_connect):
        mock_connection = unittest.mock.Mock()
        mock_cursor = unittest.mock.Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_body = {
            "body": '{"fecha": "2024-07-07", "descripcion": "Incidencia de prueba", "status": "abierto"'
            # JSON incompleto que causará un json.JSONDecodeError
        }

        # Ejecutar lambda_handler con el mock de entrada
        result = app.lambda_handler(mock_body, None)

        # Verificar el código de estado y el mensaje de error esperado
        status_code = result['statusCode']
        self.assertEqual(status_code, 400)
        self.assertIn('error', json.loads(result['body']))

if __name__ == '__main__':
    unittest.main()

