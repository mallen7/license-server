import json
from shared.logger import log_event
from shared.db_utils import insert_record

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

def registerProduct(event, context):
    """
    Registers a new product in the system.
    """
    if 'productName' not in event or 'description' not in event:
        log_event('registerProduct', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        product_name = event['productName']
        description = event['description']

        # Insert new product into the database
        insert_query = "INSERT INTO products (ProductName, Description) VALUES (%s, %s)"
        insert_record(insert_query, (product_name, description))

        return {'statusCode': 201, 'body': json.dumps('Product Registered Successfully')}

    except Exception as e:
        log_event('registerProduct', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
