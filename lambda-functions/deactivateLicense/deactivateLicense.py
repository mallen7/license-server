import json
import boto3
import datetime
from shared.logger import log_event

def deactivateLicense(event, context):
    if 'licenseKey' not in event or 'deviceID' not in event:
        log_event('deactivateLicense', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        # Deactivation logic...

        return {'statusCode': 200, 'body': json.dumps('License Deactivated Successfully')}

    except Exception as e:
        log_event('deactivateLicense', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
