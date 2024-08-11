import unittest
import json
import os
from unittest.mock import patch
from BackEndIncidencias.create_incidence.app import lambda_handler
from mysql.connector import Error

# Clases simuladas para los errores

class MockConnectionDBError:
    def cursor(self):
        return MockCursorDBError()
class MockConnectionSuccess:
    def close(self):
        pass

class MockCursorDBError:
    def execute(self, sql, params):
        raise Error("Error al insertar en la base de datos")

    def close(self):
        pass

class MockConnectionBase64Error:
    def cursor(self):
        return MockCursorBase64Error()

    def close(self):
        pass

class MockCursorBase64Error:
    def execute(self, sql, params):
        return

    def close(self):
        pass

class MockS3Client:
    def upload_fileobj(self, file, bucket, key):
        raise Exception("Error al subir el archivo a S3")

class TestCreateIncidenceLambda(unittest.TestCase):
    def setUp(self):
        # Configura las variables de entorno para conectar a la base de datos y S3 bucket de prueba
        os.environ['RDS_HOST'] = 'test_host'
        os.environ['RDS_USER'] = 'test_user'
        os.environ['RDS_PASSWORD'] = 'test_password'
        os.environ['RDS_DB'] = 'test_database'
        os.environ['S3_BUCKET'] = 'test_bucket'

    def tearDown(self):
        # Limpia las variables de entorno después de cada prueba
        os.environ.pop('RDS_HOST')
        os.environ.pop('RDS_USER')
        os.environ.pop('RDS_PASSWORD')
        os.environ.pop('RDS_DB')
        os.environ.pop('S3_BUCKET')

    def test_successful_incidence_creation(self):
        # Datos simulados del evento que representa un cuerpo de solicitud válida
        data = {
            'titulo': 'Incidente de Prueba',
            'fecha': '2024-01-01',
            'descripcion': 'Descripción detallada del incidente.',
            'estatus': 1,
            'fto_base64': 'b64_encoded_data_here'  # Esta debería ser una cadena base64 válida
        }
        event = {'body': json.dumps(data)}
        context = {}

        # Ejecutar la función Lambda con los datos de prueba
        with patch('mysql.connector.connect', return_value=MockConnectionDBError()):
            response = lambda_handler(event, context)

        # Comprobar si la respuesta es la esperada
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), 'Incidencia creada exitosamente')

    def test_missing_parameters(self):
        # Datos simulados del evento con parámetros faltantes
        data = {
            'titulo': 'Incidente de Prueba',
            'fecha': '2024-01-01',
            'descripcion': 'Descripción detallada del incidente.'
            # faltan 'estatus' y 'fto_base64'
        }
        event = {'body': json.dumps(data)}
        context = {}

        # Ejecutar la función Lambda con los datos de prueba
        response = lambda_handler(event, context)

        # Comprobar si la respuesta es la esperada
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Faltan parámetros requeridos', json.loads(response['body'])['error'])

    def test_base64_decoding_error(self):
        # Datos simulados del evento con codificación base64 incorrecta
        data = {
            'titulo': 'Incidente de Prueba',
            'fecha': '2024-01-01',
            'descripcion': 'Descripción detallada del incidente.',
            'estatus': 1,
            'fto_base64': 'invalid_base64'  # Esta debería ser una cadena base64 inválida
        }
        event = {'body': json.dumps(data)}
        context = {}

        # Ejecutar la función Lambda con los datos de prueba
        with patch('mysql.connector.connect', return_value=MockConnectionSuccess()), \
             patch('BackEndIncidencias.create_incidence.app.base64.b64decode', side_effect=Exception("Base64 decode error")):
            response = lambda_handler(event, context)

        # Comprobar si la respuesta es la esperada
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Error al decodificar la imagen', json.loads(response['body'])['error'])

    def test_db_insertion_error(self):
        # Datos simulados del evento que genera un error en la base de datos
        data = {
            'titulo': 'Incidente de Prueba',
            'fecha': '2024-01-01',
            'descripcion': 'Descripción detallada del incidente.',
            'estatus': 1,
            'fto_base64': 'b64_encoded_data_here'
        }
        event = {'body': json.dumps(data)}
        context = {}

        # Ejecutar la función Lambda con los datos de prueba
        with patch('mysql.connector.connect', return_value=MockConnectionDBError()):
            response = lambda_handler(event, context)

        # Comprobar si la respuesta es la esperada
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error al insertar en la base de datos', json.loads(response['body'])['error'])

    def test_s3_upload_error(self):
        # Datos simulados del evento que genera un error al subir el archivo a S3
        data = {
            'titulo': 'Incidente de Prueba',
            'fecha': '2024-01-01',
            'descripcion': 'Descripción detallada del incidente.',
            'estatus': 1,
            'fto_base64': 'b64_encoded_data_here'
        }
        event = {'body': json.dumps(data)}
        context = {}

        # Ejecutar la función Lambda con el error en la subida a S3
        with patch('mysql.connector.connect', return_value=MockConnectionSuccess()), \
             patch('BackEndIncidencias.create_incidence.app.S3Client.upload_fileobj', side_effect=Exception("Error al subir el archivo a S3")):
            response = lambda_handler(event, context)

        # Comprobar si la respuesta es la esperada
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error al subir el archivo a S3', json.loads(response['body'])['error'])

if __name__ == '__main__':
    unittest.main()
