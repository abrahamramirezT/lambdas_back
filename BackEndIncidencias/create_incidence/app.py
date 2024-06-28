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

        data = json.loads(event['body'])
        fecha = data['fecha']
        descripcion = data['descripcion']
        status = data['status']

        sql = "INSERT INTO reportes_incidencias (fecha, descripcion, status) VALUES (%s, %s, %s)"
        cursor.execute(sql, (fecha, descripcion, status))
        connection.commit()

        return {
            'statusCode': 201,
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
