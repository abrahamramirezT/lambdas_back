import json
import os
import mysql.connector
from mysql.connector import Error
import logging
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import base64
import uuid

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret(secret_name: str, region_name: str) -> dict:
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

def lambda_handler(event, __):
    logger.info(f"Evento recibido: {json.dumps(event)}")  # Agregar logging para debugging

    secret_name = os.environ['MY_SECRET_NAME']
    region_name = os.environ['MY_AWS_REGION']
    bucket_name = os.environ['S3_BUCKET']

    headers = {
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'POST,OPTIONS',
        'Access-Control-Allow-Origin': '*',
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

        titulo = data.get('titulo')
        fecha = data.get('fecha')
        descripcion = data.get('descripcion')
        estudiante = data.get('estudiante')
        aula = data.get('aula')
        edificio = data.get('edificio')
        matricula = data.get('matricula')
        grado = data.get('grado')
        grupo = data.get('grupo')
        div_academica = data.get('div_academica')
        estatus = data.get('estatus')
        fto_base64 = data.get('fto_base64')
        logger.info(f"Datos recibidos: {data}")  # Agregar logging para debugging

        # Validar que todos los campos necesarios estén presentes
        if not all([titulo, fecha, descripcion, estudiante, aula, edificio, matricula, estatus, grado, grupo, div_academica is not None, fto_base64]):
            raise KeyError('Faltan parámetros requeridos en la solicitud')

        # Decodificar la imagen de base64
        try:
            fto_data = base64.b64decode(fto_base64)
            fto_key = f"{uuid.uuid4()}.jpg"  # Generar un nombre único utilizando UUID
        except Exception as e:
            logger.error(f"Error al decodificar la imagen: {str(e)}")
            raise ValueError('La imagen no está en un formato base64 válido')

        # Subir la imagen a S3
        try:
            s3_client.put_object(Bucket=bucket_name, Key=fto_key, Body=fto_data, ContentType='image/jpeg')
            fto_url = f"https://{bucket_name}.s3.amazonaws.com/{fto_key}"
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error al subir la imagen a S3: {str(e)}")
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Error al subir la imagen a S3'})
            }

        # Insertar datos en la base de datos
        sql = """
        INSERT INTO reportes_incidencias (titulo, fecha, descripcion, estudiante, aula, edificio, matricula, grado, grupo, div_academica, estatus, fto_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """
        cursor.execute(sql, (titulo, fecha, descripcion, estudiante, aula, edificio, matricula,grado, grupo,div_academica, estatus, fto_url))
        connection.commit()

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('Incidencia creada exitosamente')
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
