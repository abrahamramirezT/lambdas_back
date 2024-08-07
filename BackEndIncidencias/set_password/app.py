import json
import boto3
from botocore.exceptions import ClientError
import logging
from typing import Dict

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret(secret_name: str, region_name: str) -> Dict[str, str]:
    """
    Retrieves the secret value from AWS Secrets Manager.

    Args:
        secret_name (str): The name or ARN of the secret to retrieve.
        region_name (str): The AWS region where the secret is stored.

    Returns:
        dict: The secret value retrieved from AWS Secrets Manager.
    """
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        logger.error("Failed to retrieve secret: %s", e)
        raise e

    return json.loads(get_secret_value_response['SecretString'])

def lambda_handler(event, context):
    secret_name = os.environ['MY_COGNITO_SECRET_NAME']
    region_name = os.environ['MY_AWS_REGION']

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    }

    try:
        # Obtener credenciales del App Client desde Secrets Manager
        secret = get_secret(secret_name, region_name)
        user_pool_id = secret['userPoolId']
        client_id = secret['clientId']
        # Si necesitas clientSecret, agrégalo también en Secrets Manager y recupéralo aquí
        # client_secret = secret['clientSecret']

        client = boto3.client('cognito-idp', region_name=region_name)

        # Parsea el body del evento
        body_parameters = json.loads(event["body"])
        username = body_parameters.get('username')
        temporary_password = body_parameters.get('temporary_password')
        new_password = body_parameters.get('new_password')

        # Autentica al usuario con la contraseña temporal
        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': temporary_password
            }
        )

        if response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
            client.respond_to_auth_challenge(
                ClientId=client_id,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                Session=response['Session'],
                ChallengeResponses={
                    'USERNAME': username,
                    'NEW_PASSWORD': new_password,
                    'email': username
                }
            )
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps('Contraseña cambiada exitosamente')
            }
        else:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps('No se requiere cambiar la contraseña')
            }

    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f'Error de cliente: {str(e)}')
        }
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps(f'Error al decodificar JSON: {str(e)}')
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f'Error inesperado: {str(e)}')
        }
