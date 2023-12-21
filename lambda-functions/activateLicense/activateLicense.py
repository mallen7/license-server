import json
import boto3
import datetime

def activateLicense(event, context):
    if 'licenseKey' not in event or 'productID' not in event or 'userID' not in event or 'deviceID' not in event:
        log_event('activateLicense', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        # Activation logic...

        return {'statusCode': 200, 'body': json.dumps('License Activated Successfully')}

    except Exception as e:
        log_event('activateLicense', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
