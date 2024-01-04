import json
from shared.logger import log_event
from shared.db_utils import execute_query

def deactivateLicense(event, context):
    """
    Deactivates a license in the system.
    """
    if 'licenseKey' not in event or 'deviceID' not in event:
        log_event('deactivateLicense', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        license_key = event['licenseKey']
        device_id = event['deviceID']

        # Update the license status in the database
        update_query = "UPDATE licenses SET IsActive = %s WHERE LicenseKey = %s AND DeviceID = %s"
        execute_query(update_query, (False, license_key, device_id))

        return {'statusCode': 200, 'body': json.dumps('License Deactivated Successfully')}

    except Exception as e:
        log_event('deactivateLicense', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
