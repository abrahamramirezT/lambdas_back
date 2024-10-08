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
        logger.error("Failed to retrieve secret: %s", e)
        raise e

    return json.loads(get_secret_value_response['SecretString'])

def lambda_handler(event, context):
    secret_name = os.environ['MY_SECRET_NAME']
    region_name = os.environ['MY_AWS_REGION']

    headers = {
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'PUT,OPTIONS',
        'Access-Control-Allow-Origin': '*',
    }

    try:
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

        # Cargar datos del evento
        data = json.loads(event['body'])
        id = data['id']
        estatus = data['estatus']

        # Actualizar el estatus del reporte
        sql = """
        UPDATE reportes_incidencias
        SET estatus = %s
        WHERE id = %s
        """
        cursor.execute(sql, (estatus, id))
        connection.commit()

        if cursor.rowcount > 0:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps('Estatus del reporte actualizado correctamente')
            }
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps('Reporte no encontrado')
            }
    except KeyError as e:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps(f'Bad request. Missing required parameter: {str(e)}')
        }
    except mysql.connector.Error as err:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f"Database error: {str(err)}")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f"Error: {str(e)}")
        }
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
