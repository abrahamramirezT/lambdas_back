import json
import os
import mysql.connector
from mysql.connector import Error
import logging

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    try:
        db_host = os.environ['RDS_HOST']
        db_user = os.environ['RDS_USER']
        db_password = os.environ['RDS_PASSWORD']
        db_name = os.environ['RDS_DB']

        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        cursor = connection.cursor()

        # Cargar datos del evento
        data = json.loads(event['body'])
        titulo = data.get('titulo')
        fecha = data.get('fecha')
        descripcion = data.get('descripcion')
        estatus = data.get('estatus')
        fto_url = data.get('fto_url')  # Asegúrate de que la URL de la foto esté presente

        # Validar que todos los campos necesarios estén presentes
        if not all([titulo, fecha, descripcion, estatus is not None, fto_url]):
            raise KeyError('Faltan parámetros requeridos en la solicitud')

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
    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar JSON: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Solicitud incorrecta. El cuerpo debe ser un JSON válido.'})
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
