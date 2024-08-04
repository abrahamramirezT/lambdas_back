import json
import os
import mysql.connector

def lambda_handler(event, context):
    try:
        db_host = os.environ['RDS_HOST']
        db_user = os.environ['RDS_USER']
        db_password = os.environ['RDS_PASSWORD']
        db_name = os.environ['RDS_DB']

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
        titulo = data["titulo"]
        fecha = data['fecha']
        descripcion = data['descripcion']
        estatus = data['estatus']
        reporte_id = data['reporte_id']  # Asegúrate de incluir reporte_id

        # Actualizar reporte
        sql = """
        UPDATE reportes_incidencias
        SET titulo = %s, fecha = %s, descripcion = %s, estatus = %s
        WHERE reporte_id = %s
        """
        cursor.execute(sql, (titulo, fecha, descripcion, estatus, reporte_id))  # Asegúrate de incluir reporte_id
        connection.commit()

        if cursor.rowcount > 0:
            return {
                'statusCode': 200,
                'body': json.dumps('Reporte actualizado correctamente')
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Reporte no encontrado')
            }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Bad request. Missing required parameter: {str(e)}')
        }
    except mysql.connector.Error as err:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Database error: {str(err)}")
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
