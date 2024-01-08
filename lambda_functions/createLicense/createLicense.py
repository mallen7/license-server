import json
import boto3
import uuid
from shared.logger import log_event
from shared.db_utils import insert_record

def get_api_key():
    """Retrieve the API key from AWS Secrets Manager."""
    log_event('createLicense', 'Info', 'Retrieving API key from Secrets Manager', {})
    secret_name = "LicenseAPIKey"  # Replace with the name of your secret
    region_name = "us-east-1"  # Replace with your AWS region

    client = boto3.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)['apiKey']

def validate_api_key(api_key):
    """Validate the provided API key."""
    log_event('createLicense', 'Info', 'Validating API key', {})
    stored_api_key = get_api_key()
    return api_key == stored_api_key

def createLicense(event, context):
    """
    Creates a new license in the system.
    """
    log_event('createLicense', 'Info', 'Function invoked', event)

    if 'productID' not in event or 'userID' not in event or 'expiryDate' not in event:
        log_event('createLicense', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        product_id = event['productID']
        user_id = event['userID']
        expiry_date = event['expiryDate']

        # Check if a license already exists for the given productID and userID
        check_query = "SELECT * FROM licenses WHERE ProductID = %s AND UserID = %s"
        existing_license = fetch_one(check_query, (product_id, user_id))
        if existing_license:
            log_event('createLicense', 'Warning', 'License already exists', {'productID': product_id, 'userID': user_id})
            return {'statusCode': 409, 'body': json.dumps('License already exists')}

        license_key = str(uuid.uuid4())  # Generate a random UUID as license key
        log_event('createLicense', 'Info', 'Creating new license', {'licenseKey': license_key})

        # Insert new license into the database
        insert_query = "INSERT INTO licenses (LicenseKey, ProductID, UserID, ExpiryDate) VALUES (%s, %s, %s, %s)"
        insert_record(insert_query, (license_key, product_id, user_id, expiry_date))
        log_event('createLicense', 'Info', 'License created successfully', {'licenseKey': license_key})

        return {'statusCode': 201, 'body': json.dumps('License Created Successfully')}

    except Exception as e:
        log_event('createLicense', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}