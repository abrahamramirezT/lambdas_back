import json
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime

def lambda_handler(event, context):
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

        # Obtener el identificador del reporte del parámetro de ruta
        reporte_id = event['pathParameters']['reporte_id']

        # Consulta de un reporte específico
        sql = "SELECT * FROM reportes_incidencias WHERE reporte_id = %s"
        cursor.execute(sql, (reporte_id,))
        reporte = cursor.fetchone()

        if reporte:
            # Manejo de la fecha
            reporte_date = reporte[2]  # El índice debe coincidir con la columna 'fecha'
            if isinstance(reporte_date, str):
                reporte_date = datetime.strptime(reporte_date, '%Y-%m-%d').date()
            # Convertir la fecha a cadena antes de incluirla en el JSON
            reporte_date_joined_str = reporte_date.strftime('%Y-%m-%d')

            data = {
                'reporte_id': reporte[0],  # Identificador único
                'titulo': reporte[1],
                'fecha': reporte_date_joined_str,
                'descripcion': reporte[3],
                'estatus': reporte[4],
                'fto_url': reporte[5]
            }
            return {
                'statusCode': 200,
                'body': json.dumps(data)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Reporte no encontrado'})
            }
    except Error as e:
        error_message = f"Error de conexión a la base de datos: {str(e)}"
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }
    except KeyError as e:
        error_message = f"Falta la clave esperada en el evento: {str(e)}"
        return {
            'statusCode': 400,
            'body': json.dumps({'error': error_message})
        }
    except Exception as error:
        error_message = f"Error inesperado: {str(error)}"
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
