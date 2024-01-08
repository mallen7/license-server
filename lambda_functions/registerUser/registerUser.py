import json
import boto3
from shared.db_utils import insert_record
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

def registerUser(event, context):
    """
    Registers a new user in the system.
    """
    log_event('registerUser', 'Info', 'Function invoked', event)

    if 'name' not in event or 'email' not in event or 'company' not in event:
        log_event('registerUser', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        name = event['name']
        email = event['email']
        company = event['company']

        # Check if the user already exists
        check_query = "SELECT * FROM users WHERE Email = %s"
        existing_user = fetch_one(check_query, (email,))
        if existing_user:
            log_event('registerUser', 'Warning', 'User already exists', {'email': email})
            return {'statusCode': 409, 'body': json.dumps('User already exists')}

        # Insert new user into the database
        log_event('registerUser', 'Info', 'Inserting new user', {'email': email})
        insert_query = "INSERT INTO users (Name, Email, Company) VALUES (%s, %s, %s)"
        insert_record(insert_query, (name, email, company))
        log_event('registerUser', 'Info', 'User registered successfully', {'email': email})

        return {'statusCode': 201, 'body': json.dumps('User Registered Successfully')}

    except Exception as e:
        log_event('registerUser', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}