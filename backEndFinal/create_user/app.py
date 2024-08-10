import json
import os
import mysql.connector
from mysql.connector import Error
import logging
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import base64

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret(secret_name: str, region_name: str) -> Dict[str, str]:
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        logging.error("Failed to retrieve secret: %s", e)
        raise e

    return json.loads(get_secret_value_response['SecretString'])

def lambda_handler(event, context):
    logger.info(f"Evento recibido: {json.dumps(event)}")  # Agregar logging para debugging
    secret_name = os.environ['MY_SECRET_NAME']
    region_name = os.environ['MY_AWS_REGION']
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',

    }
    try:
        # Parámetros de conexión a la base de datos
        secret = get_secret(secret_name, region_name)
        db_host = secret['host']
        db_user = secret['username']
        db_password = secret['password']
        db_name = secret['dbname']




        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        cursor = connection.cursor()

        # Cargar datos del evento
        try:
            data = json.loads(event['body'])
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON: {str(e)}")
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Solicitud incorrecta. El cuerpo debe ser un JSON válido.'})
            }


        username = data.get('username')
        password = data.get('password')

        logger.info(f"Datos recibidos: {data}")  # Agregar logging para debugging

        # Validar que todos los campos necesarios estén presentes
        if not all([username, password is not None]):
            raise KeyError('Faltan parámetros requeridos en la solicitud')


        # Insertar datos en la base de datos
        sql = """
        INSERT INTO users_incidencias (username, password)
        VALUES (%s, %s)
        """
        cursor.execute(sql, (username, password))
        connection.commit()

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('User creado exitosamente')
        }

    except KeyError as e:
        logger.error(f"Faltan parámetros requeridos en la solicitud: {str(e)}")
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'Solicitud incorrecta. Faltan parámetros requeridos.'})
        }
    except Error as e:
        logger.error(f"Error de base de datos: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Error de base de datos'})
        }
    except ValueError as e:
        logger.error(f"Error en la imagen: {str(e)}")
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Error inesperado'})
        }
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()