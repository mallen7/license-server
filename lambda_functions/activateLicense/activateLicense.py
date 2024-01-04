import json
from shared.db_utils import execute_query
import shared.logger as logger

def activateLicense(event, context):
    """
    Activates a license in the system.
    """
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
