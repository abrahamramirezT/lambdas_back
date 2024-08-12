import base64
import unittest
import json
import boto3
import os
from moto import mock_s3, mock_secretsmanager
import mysql.connector
from create_incidence.app import lambda_handler  # Importa tu lambda desde el módulo correcto

class TestLambdaHandler(unittest.TestCase):

    @mock_s3
    @mock_secretsmanager
    def test_lambda_handler_success(self):
        # Configurar el entorno
        os.environ['MY_SECRET_NAME'] = 'test_secret'
        os.environ['MY_AWS_REGION'] = 'us-east-1'
        os.environ['S3_BUCKET'] = 'test-bucket'

        # Simular Secrets Manager
        client = boto3.client('secretsmanager', region_name='us-east-1')
        secret = {
            'host': 'localhost',
            'username': 'test_user',
            'password': 'test_pass',
            'dbname': 'test_db'
        }
        client.create_secret(Name='test_secret', SecretString=json.dumps(secret))

        # Simular S3
        s3_client = boto3.client('s3', region_name='us-east-1')
        s3_client.create_bucket(Bucket='test-bucket')

        # Simular base de datos MySQL en memoria
        connection = mysql.connector.connect(
            host="localhost",
            user="test_user",
            password="test_pass",
            database="test_db"
        )
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE reportes_incidencias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255),
            fecha VARCHAR(255),
            descripcion TEXT,
            estatus INT,
            fto_url VARCHAR(255),
            user_id INT
        )
        """)
        connection.commit()

        # Crear evento de prueba
        event = {
            'body': json.dumps({
                'titulo': 'Incidente 1',
                'fecha': '2024-08-12',
                'descripcion': 'Descripción del incidente',
                'estatus': 1,
                'fto_base64': base64.b64encode(b'Test image data').decode('utf-8'),
                'user_id': 123
            })
        }

        # Ejecutar la lambda
        response = lambda_handler(event, None)

        # Validar la respuesta
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), 'Incidencia creada exitosamente')

        # Validar que la imagen se subió a S3
        s3_response = s3_client.get_object(Bucket='test-bucket', Key='Incidente_1_2024-08-12.jpg')
        self.assertEqual(s3_response['Body'].read(), b'Test image data')

        # Validar que los datos se insertaron en la base de datos
        cursor.execute("SELECT * FROM reportes_incidencias WHERE titulo='Incidente 1'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'Incidente 1')

    # Aquí puedes añadir más pruebas para los diferentes escenarios de error

if __name__ == '__main__':
    unittest.main()
