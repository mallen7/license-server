import json
import boto3
import datetime
from shared.logger import log_event

def createLicense(event, context):
    if 'productID' not in event or 'userID' not in event or 'expiryDate' not in event:
        log_event('createLicense', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        # License creation logic...

        return {'statusCode': 200, 'body': json.dumps('License Created Successfully')}

    except Exception as e:
        log_event('createLicense', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
