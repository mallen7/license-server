import json
import boto3
from shared.db_utils import execute_query
import shared.logger as logger

def get_api_key():
    """Retrieve the API key from AWS Secrets Manager."""
    secret_name = "LicenseAPIKey"  # Replace with the name of your secret
    region_name = "us-east-1"  # Replace with your AWS region

    client = boto3.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)['apiKey']

def validate_api_key(api_key):
    """Validate the provided API key."""
    stored_api_key = get_api_key()
    return api_key == stored_api_key

def activateLicense(event, context):
    """
    Activates a license in the system.
    """
    # API Key validation
    api_key = event.get('headers', {}).get('x-api-key')
    if not api_key or not validate_api_key(api_key):
        return {'statusCode': 403, 'body': json.dumps('Forbidden: Invalid API Key')}

    # Check for required parameters
    if 'licenseKey' not in event or 'productID' not in event or 'userID' not in event or 'deviceID' not in event:
        logger.log_event('activateLicense', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        license_key = event['licenseKey']
        product_id = event['productID']
        user_id = event['userID']

        # Update the license activation status in the database
        update_query = "UPDATE licenses SET IsActive = %s WHERE LicenseKey = %s AND ProductID = %s AND UserID = %s"
        execute_query(update_query, (True, license_key, product_id, user_id))

        # Additional logic for device ID association if required
        # ...

        return {'statusCode': 200, 'body': json.dumps('License Activated Successfully')}

    except Exception as e:
        logger.log_event('activateLicense', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
