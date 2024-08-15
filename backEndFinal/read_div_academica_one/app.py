import json
import os
import mysql.connector
from mysql.connector import Error
import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict

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

def lambda_handler(event, __):
    # Obtener variables de entorno
    secret_name = os.environ['MY_SECRET_NAME']
    region_name = os.environ['MY_AWS_REGION']

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    }

    try:
        # Obtener las credenciales de la base de datos desde Secrets Manager
        secret = get_secret(secret_name, region_name)
        db_host = secret['host']
        db_user = secret['username']
        db_password = secret['password']
        db_name = secret['dbname']

        # Obtener el ID del reporte desde el evento
        div_aca_id = event['pathParameters']['div_aca_id']
        if not div_aca_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'El parámetro ID es requerido'})
            }

        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        # Consulta del reporte específico por ID
        sql = "SELECT * FROM divisiones_academicas WHERE div_aca_id = %s"
        cursor.execute(sql, (div_aca_id,))
        div_aca = cursor.fetchone()

        if div_aca:
            try:
                div_aca_dict = {
                    'div_aca_id': div_aca[0],
                    'nombre': div_aca[1]

                }
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(div_aca_dict)
                }
            except Exception as e:
                logger.error(f"Error al procesar el reporte {div_aca}: {str(e)}")
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'error': 'Error al procesar el reporte'})
                }
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': f"No se encontró el reporte con ID {div_aca_id}"})
            }

    except Error as e:
        logger.error(f"Error de base de datos: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Error de base de datos'})
        }
    except KeyError as e:
        logger.error(f"Clave faltante en el evento: {str(e)}")
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': f"Clave faltante en el evento: {str(e)}"})
        }
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Error inesperado', 'message': str(e)})
        }
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
