import json
import boto3
import os

app_client_id = os.environ.get('USER_POOL_CLIENT_ID')
client = boto3.client('cognito-idp')

def handler(event, context):
    try:
        body = json.loads(event['body'])
        email = body['email']
        password = body['password']
        
        response = client.initiate_auth(
            ClientId= app_client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User signed in successfully!', 'token': response['AuthenticationResult']['IdToken']})
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': str(e)})
        }
