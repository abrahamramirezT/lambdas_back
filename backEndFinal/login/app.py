import json
import os
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

def lambda_handler(event, __):
    # Obtener el nombre del secreto y la región de las variables de entorno
    secret_name = os.environ['MY_COGNITO_SECRET_NAME']
    region_name = os.environ['MY_AWS_REGION']

    # Recuperar los secretos
    secret = get_secret(secret_name, region_name)
    client_id = secret['client_id']
    user_pool_id = secret['user_pool_id']

    client = boto3.client('cognito-idp', region_name='us-east-1')

    headers = {
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'POST,OPTIONS',
        'Access-Control-Allow-Origin': '*'
    }

    try:
        body_parameters = json.loads(event["body"])
        username = body_parameters.get('username')
        password = body_parameters.get('password')

        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        id_token = response['AuthenticationResult']['IdToken']
        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']

        # Obtén los grupos del usuario
        user_groups = client.admin_list_groups_for_user(
            Username=username,
            UserPoolId=user_pool_id
        )

        # Determina el rol basado en el grupo
        role = None
        if user_groups['Groups']:
            role = user_groups['Groups'][0]['GroupName']  # Asumiendo un usuario pertenece a un solo grupo

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'id_token': id_token,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'role': role
            })
        }

    except ClientError as e:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({"error_message": e.response['Error']['Message']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error_message": str(e)})
        }
