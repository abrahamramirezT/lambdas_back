import json
import os
import mysql.connector
from datetime import date

def lambda_handler(event, context):
    # Obtener variables de entorno
    db_host = os.environ['RDS_HOST']
    db_user = os.environ['RDS_USER']
    db_password = os.environ['RDS_PASSWORD']
    db_name = os.environ['RDS_DB']

    # Conexión a la base de datos
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        cursor = connection.cursor()

        reporte_id = event['pathParameters']['reporte_id']

        sql = "SELECT * FROM reportes_incidencias WHERE reporte_id = %s"
        cursor.execute(sql, (reporte_id,))
        admin = cursor.fetchone()

        if admin:
            # Convertir la fecha a cadena de texto antes de serializar a JSON
            reporte_date_joined_str = admin[1].strftime('%Y-%m-%d')
            user_dict = {
                'reporte_id': admin[0],
                'fecha': reporte_date_joined_str,
                'descripcion': admin[2],
                'status': admin[3],

            }
            return {
                'statusCode': 200,
                'body': json.dumps(user_dict)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Reporte no encontrado')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()