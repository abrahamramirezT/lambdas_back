import json
import os
import mysql.connector
from mysql.connector import Error
import logging
import boto3
from botocore.exceptions import ClientError
from typing import Dict

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret(secret_name: str, region_name: str) -> Dict[str, str]:
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        logging.error("Failed to retrieve secret: %s", e)
        raise e

    return json.loads(get_secret_value_response['SecretString'])

def lambda_handler(event, __):
    # Obtener variables de entorno
    secret_name = os.environ['MY_SECRET_NAME']
    region_name = os.environ['MY_AWS_REGION']

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    }

    try:
        # Obtener las credenciales de la base de datos desde Secrets Manager
        secret = get_secret(secret_name, region_name)
        db_host = secret['host']
        db_user = secret['username']
        db_password = secret['password']
        db_name = secret['dbname']

        # Obtener el ID del reporte desde el evento
        id = event['pathParameters']['id']
        if not id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'El parámetro ID es requerido'})
            }

        # Conexión a la base de datos
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        # Consulta del reporte específico por ID
        sql = """
        SELECT 
            r.id,
            r.titulo,
            r.fecha,
            r.descripcion,
            r.estudiante,
            a.nombre AS aula_nombre,
            e.nombre AS edificio_nombre,
            r.matricula,
            g.nombre AS grado_nombre,
            grp.nombre AS grupo_nombre,
            d.nombre AS div_academica_nombre,
            r.estatus,
            r.fto_url
        FROM 
            reportes_incidencias r
        JOIN 
            aulas a ON r.aula = a.aula_id
        JOIN 
            edificios e ON r.edificio = e.edificio_id
        JOIN 
            grado g ON r.grado = g.grado_id
        JOIN 
            grupo grp ON r.grupo = grp.grupo_id
        JOIN 
            divisiones_academicas d ON r.div_academica = d.div_aca_id
        WHERE 
            r.id = %s;
        """
        cursor.execute(sql, (id,))
        reporte = cursor.fetchone()

        if reporte:
            try:
                # Convertir la fecha a cadena de texto antes de serializar a JSON
                reporte_date_joined_str = reporte[2].strftime('%Y-%m-%d')
                reporte_dict = {
                    'id': reporte[0],
                    'titulo': reporte[1],
                    'fecha': reporte_date_joined_str,
                    'descripcion': reporte[3],
                    'estudiante': reporte[4],
                    'aula_nombre': reporte[5],
                    'edificio_nombre': reporte[6],
                    'matricula': reporte[7],
                    'grado_nombre': reporte[8],
                    'grupo_nombre': reporte[9],
                    'div_academica_nombre': reporte[10],
                    'estatus': reporte[11],
                    'fto_url': reporte[12]
                }
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(reporte_dict)
                }
            except Exception as e:
                logger.error(f"Error al procesar el reporte {reporte}: {str(e)}")
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'error': 'Error al procesar el reporte'})
                }
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': f"No se encontró el reporte con ID {id}"})
            }

    except Error as e:
        logger.error(f"Error de base de datos: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Error de base de datos'})
        }
    except KeyError as e:
        logger.error(f"Clave faltante en el evento: {str(e)}")
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': f"Clave faltante en el evento: {str(e)}"})
        }
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Error inesperado', 'message': str(e)})
        }
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()
