import json
import datetime
from shared.db_utils import insert_record, get_db_connection
from shared.logger import log_event

def registerUser(event, context):
    """
    Registers a new user in the system.
    """
    if 'name' not in event or 'email' not in event or 'company' not in event:
        log_event('registerUser', 'Error', 'Invalid input', event)
        return {'statusCode': 400, 'body': json.dumps('Bad Request: Missing required parameters')}

    try:
        name = event['name']
        email = event['email']
        company = event['company']

        # Insert new user into the database
        insert_query = "INSERT INTO users (Name, Email, Company) VALUES (%s, %s, %s)"
        insert_record(insert_query, (name, email, company))

        return {'statusCode': 201, 'body': json.dumps('User Registered Successfully')}

    except Exception as e:
        log_event('registerUser', 'Error', str(e), event)
        return {'statusCode': 500, 'body': json.dumps('Internal Server Error')}
