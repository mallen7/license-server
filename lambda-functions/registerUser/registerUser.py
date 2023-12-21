import json
import boto3
import datetime
from shared.logger import log_event

def registerUser(event, context):
    if 'name' not in event or 'email' not in event or 'company' not in event:
        log_event('registerUser', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        # User registration logic...

        return {'statusCode': 200, 'body': json.dumps('User Registered Successfully')}

    except Exception as e:
        log_event('registerUser', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
