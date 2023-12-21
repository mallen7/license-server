import json
import datetime
from shared.logger import log_event
from shared.db_utils import insert_record

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
