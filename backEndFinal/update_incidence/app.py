import json
import os
import mysql.connector
from mysql.connector import Error
import logging
import boto3
from botocore.exceptions import ClientError, BotoCoreError
import base64
import uuid
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

# Crear el cliente de S3
s3_client = boto3.client('s3', region_name='us-east-1')

def lambda_handler(event, context):
    secret_name = os.environ['MY_SECRET_NAME']
    region_name = os.environ['MY_AWS_REGION']
    bucket_name = os.environ['S3_BUCKET']

    headers = {
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'POST,OPTIONS',
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
        fto_base64 = data.get('fto_base64')  # Obtener la imagen si se envía

        fto_url = None
        if fto_base64:
            # Decodificar la imagen de base64 y subirla a S3
            try:
                fto_data = base64.b64decode(fto_base64)
                fto_key = f"{str(uuid.uuid4())}.jpg"  # Generar un nombre único utilizando UUID
                s3_client.put_object(Bucket=bucket_name, Key=fto_key, Body=fto_data, ContentType='image/jpeg')
                fto_url = f"https://{bucket_name}.s3.amazonaws.com/{fto_key}"
            except Exception as e:
                logger.error(f"Error al procesar la imagen: {str(e)}")
                raise ValueError('Error al procesar la imagen')

        # Actualizar reporte
        if fto_url:
            sql = """
            UPDATE reportes_incidencias
            SET estatus = %s 
            WHERE id = %s
            """
            cursor.execute(sql, (estatus, fto_url, id))
        else:
            sql = """
            UPDATE reportes_incidencias
            SET estatus = %s, fto_url = %s
            WHERE id = %s
            """
            cursor.execute(sql, (estatus, id))

        connection.commit()

        if cursor.rowcount > 0:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps('Reporte actualizado correctamente')
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
    except ValueError as e:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps(f"Error: {str(e)}")
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
