import json
import boto3
from shared.db_utils import execute_query
from shared.logger import log_event

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

def validateLicense(event, context):
    """
    Validate a license key for a given product and device.
    """
    if 'licenseKey' not in event or 'productID' not in event or 'deviceID' not in event:
        log_event('validateLicense', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        license_key = event['licenseKey']
        product_id = event['productID']

        # Validate the license logic
        license = execute_query("SELECT * FROM licenses WHERE LicenseKey = %s AND ProductID = %s", (license_key, product_id), fetch_one=True)

        if not license:
            log_event('validateLicense', 'Error', 'License not found', {'licenseKey': license_key, 'productID': product_id})
            return {'statusCode': 404, 'body': json.dumps('License not found')}

        # Additional logic to validate the license based on the query result
        # ...

        return {'statusCode': 200, 'body': json.dumps('License Validated Successfully')}

    except Exception as e:
        log_event('validateLicense', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
