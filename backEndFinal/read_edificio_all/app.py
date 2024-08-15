
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

        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        # Consulta de todos los reportes
        sql = "SELECT * FROM edificios"
        cursor.execute(sql)
        edificios = cursor.fetchall()

        if edificios:
            edificios_list = []
            for edificio in edificios:
                try:
                    edificio_dict = {
                        'edificio_id': edificio[0],
                        'nombre': edificio[1]

                    }
                    edificios_list.append(edificio_dict)
                except Exception as e:
                    logger.error(f"Error al procesar el reporte {edificio}: {str(e)}")
                    continue

            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(edificios_list)
            }
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'No se encontraron reportes'})
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
