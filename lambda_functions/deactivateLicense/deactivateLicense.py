import json
import boto3
import uuid
from shared.logger import log_event
from shared.db_utils import execute_query

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

def deactivateLicense(event, context):
    """
    Deactivates a license in the system.
    """
    log_event('deactivateLicense', 'Info', 'Function invoked', event)

    if 'licenseKey' not in event or 'deviceID' not in event:
        log_event('deactivateLicense', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        license_key = event['licenseKey']
        device_id = event['deviceID']

        # Check if the license exists
        check_query = "SELECT * FROM licenses WHERE LicenseKey = %s AND DeviceID = %s"
        license_record = fetch_one(check_query, (license_key, device_id))
        if not license_record:
            log_event('deactivateLicense', 'Warning', 'License not found', {'licenseKey': license_key, 'deviceID': device_id})
            return {'statusCode': 404, 'body': json.dumps('License not found')}

        # Deactivate the license
        log_event('deactivateLicense', 'Info', 'Deactivating license', {'licenseKey': license_key, 'deviceID': device_id})
        update_query = "UPDATE licenses SET IsActive = %s WHERE LicenseKey = %s AND DeviceID = %s"
        execute_query(update_query, (False, license_key, device_id))

        log_event('deactivateLicense', 'Info', 'License deactivated successfully', {'licenseKey': license_key})
        return {'statusCode': 200, 'body': json.dumps('License Deactivated Successfully')}

    except Exception as e:
        log_event('deactivateLicense', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}