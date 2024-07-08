import json
import  unittest
from unittest.mock import patch
import mysql.connector
import mysql
from delete_incidence import app




class TestDeleteIncidence(unittest.TestCase):

    @patch.dict("os.environ", {
        "RDS_HOST": "database-incidencias.cpm62yu6ezkc.us-east-1.rds.amazonaws.com",
        "RDS_USER": "admin",
        "RDS_PASSWORD": "admin123",
        "RDS_DB": "incidencias"
    })
    @patch('mysql.connector.connect')
    def test_lambda_handler_delete_report(self, mock_connect):
        mock_connection = unittest.mock.Mock()
        mock_cursor = unittest.mock.Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_body = {
            "body": json.dumps({
                "reporte_id": 5,

            })
        }

        mock_cursor.execute.return_value = None

        result = app.lambda_handler(mock_body, None)
        status_code = result['statusCode']
        self.assertEqual(status_code, 200)
        self.assertEqual(json.loads(result['body']), 'Reporte eliminado exitosamente')
