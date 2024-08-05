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

# Crear el cliente de S3
s3_client = boto3.client('s3', region_name='us-east-1')



def lambda_handler(event, context):
    logger.info(f"Evento recibido: {json.dumps(event)}")  # Agregar logging para debugging

    try:
        # Parámetros de conexión a la base de datos
        db_host = os.environ['RDS_HOST']
        db_user = os.environ['RDS_USER']
        db_password = os.environ['RDS_PASSWORD']
        db_name = os.environ['RDS_DB']
        bucket_name = os.environ['S3_BUCKET']  # Obtener el nombre del bucket de la variable de entorno

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
                'body': json.dumps({'error': 'Solicitud incorrecta. El cuerpo debe ser un JSON válido.'})
            }

        titulo = data.get('titulo')
        fecha = data.get('fecha')
        descripcion = data.get('descripcion')
        estatus = data.get('estatus')
        fto_base64 = data.get('fto_base64')

        logger.info(f"Datos recibidos: {data}")  # Agregar logging para debugging

        # Validar que todos los campos necesarios estén presentes
        if not all([titulo, fecha, descripcion, estatus is not None, fto_base64]):
            raise KeyError('Faltan parámetros requeridos en la solicitud')

        # Decodificar la imagen de base64
        try:
            fto_data = base64.b64decode(fto_base64)
            fto_key = f"{titulo.replace(' ', '_')}_{fecha}.jpg"
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
                'body': json.dumps({'error': 'Error al subir la imagen a S3'})
            }

        # Insertar datos en la base de datos
        sql = """
        INSERT INTO reportes_incidencias (titulo, fecha, descripcion, estatus, fto_url)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (titulo, fecha, descripcion, estatus, fto_url))
        connection.commit()

        return {
            'statusCode': 200,
            'body': json.dumps('Incidencia creada exitosamente')
        }

    except KeyError as e:
        logger.error(f"Faltan parámetros requeridos en la solicitud: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Solicitud incorrecta. Faltan parámetros requeridos.'})
        }
    except Error as e:
        logger.error(f"Error de base de datos: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error de base de datos'})
        }
    except ValueError as e:
        logger.error(f"Error en la imagen: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error inesperado'})
        }
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
