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
    log_event('registerProduct', 'Info', 'Function invoked', event)

    if 'productName' not in event or 'description' not in event:
        log_event('registerProduct', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        product_name = event['productName']
        description = event['description']

        # Check if the product already exists
        check_query = "SELECT * FROM products WHERE ProductName = %s"
        existing_product = fetch_one(check_query, (product_name,))
        if existing_product:
            log_event('registerProduct', 'Warning', 'Product already exists', {'productName': product_name})
            return {'statusCode': 409, 'body': json.dumps('Product already exists')}

        # Insert new product into the database
        log_event('registerProduct', 'Info', 'Inserting new product', {'productName': product_name})
        insert_query = "INSERT INTO products (ProductName, Description) VALUES (%s, %s)"
        insert_record(insert_query, (product_name, description))
        log_event('registerProduct', 'Info', 'Product registered successfully', {'productName': product_name})

        return {'statusCode': 201, 'body': json.dumps('Product Registered Successfully')}

    except Exception as e:
        log_event('registerProduct', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}