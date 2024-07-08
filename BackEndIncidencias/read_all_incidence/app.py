
import json
import os
import mysql.connector
from mysql.connector import Error
import logging
from datetime import date

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, __):
    # Obtener variables de entorno
    db_host = os.environ['RDS_HOST']
    db_user = os.environ['RDS_USER']
    db_password = os.environ['RDS_PASSWORD']
    db_name = os.environ['RDS_DB']

    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        sql = "SELECT * FROM reportes_incidencias"
        cursor.execute(sql)
        reportes = cursor.fetchall()

        if reportes:
            reportes_list = []
            for reporte in reportes:
                # Convertir la fecha a cadena de texto antes de serializar a JSON
                reporte_date_joined_str = reporte[1].strftime('%Y-%m-%d')
                reporte_dict = {
                    'reporte_id': reporte[0],
                    'fecha': reporte_date_joined_str,
                    'descripcion': reporte[2],
                    'status': reporte[3],
                }
                reportes_list.append(reporte_dict)

            return {
                'statusCode': 200,
                'body': json.dumps(reportes_list)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No se encontraron reportes'})
            }
    except Error as e:
        logger.error(f"Error de base de datos: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error de base de datos'})
        }
    except KeyError as e:
        logger.error(f"Clave faltante en el evento: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f"Clave faltante en el evento: {str(e)}"})
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
