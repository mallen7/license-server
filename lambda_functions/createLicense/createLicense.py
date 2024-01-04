import json
from shared.logger import log_event
from shared.db_utils import insert_record

def createLicense(event, context):
    """
    Creates a new license in the system.
    """
    if 'productID' not in event or 'userID' not in event or 'expiryDate' not in event:
        log_event('createLicense', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        product_id = event['productID']
        user_id = event['userID']
        expiry_date = event['expiryDate']

        # Insert new license into the database
        insert_query = "INSERT INTO licenses (ProductID, UserID, ExpiryDate) VALUES (%s, %s, %s)"
        insert_record(insert_query, (product_id, user_id, expiry_date))

        return {'statusCode': 201, 'body': json.dumps('License Created Successfully')}

    except Exception as e:
        log_event('createLicense', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
