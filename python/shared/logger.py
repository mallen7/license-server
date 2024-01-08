import json
import pymysql
import datetime
import uuid
import boto3
from botocore.exceptions import ClientError

def get_secret():
    """Retrieve secret from AWS Secrets Manager."""
    secret_name = "LicenseDB"  # Name of the secret
    region_name = "us-east-1"  # Replace with your AWS region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print("ERROR: Could not retrieve secret -", e)
        raise e
    else:
        # Decrypts secret using the associated KMS CMK
        # Depending on whether the secret is a string or binary, one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return json.loads(decoded_binary_secret)

def get_db_connection():
    """Establishes a database connection using credentials from Secrets Manager."""
    secret = get_secret()

    try:
        connection = pymysql.connect(
            host=secret['host'],
            user=secret['username'],
            password=secret['password'],
            db=secret['dbname'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MySQL instance.")
        print(e)
        raise

def generate_unique_log_id():
    """Generates a unique identifier for a log entry."""
    return str(uuid.uuid4())

def log_event(function_name, event_type, message, additional_info=None):
    """Logs an event to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    timestamp = datetime.datetime.now()
    log_id = generate_unique_log_id()

    sql = """INSERT INTO event_logs (LogID, Timestamp, FunctionName, EventType, Message, AdditionalInfo)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (log_id, timestamp, function_name, event_type, message, json.dumps(additional_info)))
    conn.commit()

    cursor.close()
    conn.close()
