import json
import boto3
import datetime
from shared.logger import log_event

def registerProduct(event, context):
    if 'productName' not in event or 'description' not in event:
        log_event('registerProduct', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        # Product registration logic...

        return {'statusCode': 200, 'body': json.dumps('Product Registered Successfully')}

    except Exception as e:
        log_event('registerProduct', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
