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
                'body': json.dumps('No se encontraron reportes')
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
