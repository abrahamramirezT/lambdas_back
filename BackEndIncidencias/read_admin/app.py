import json
import os
import mysql.connector
from mysql.connector import Error
from datetime import date

def lambda_handler(event, context):
    # Obtener variables de entorno para la conexión a la base de datos
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

        # Obtener parámetros del cuerpo del evento JSON
        body_parameters = json.loads(event["body"])
        reporte_id = body_parameters.get('reporte_id')

        if reporte_id is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "reporte_id is required."})
            }

        # Consulta SQL para obtener el reporte según reporte_id
        sql = "SELECT * FROM reportes_incidencias WHERE reporte_id = %s"
        cursor.execute(sql, (reporte_id,))
        admin = cursor.fetchone()

        if admin:
            # Convertir la fecha a cadena de texto antes de serializar a JSON
            reporte_date_joined_str = admin[1].strftime('%Y-%m-%d')
            reporte_dict = {
                'reporte_id': admin[0],
                'fecha': reporte_date_joined_str,
                'descripcion': admin[2],
                'status': admin[3],
            }
            return {
                'statusCode': 200,
                'body': json.dumps(reporte_dict)
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
    except Exception as e:
        error_message = f"Error inesperado: {str(e)}"
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
