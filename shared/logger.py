import json
import pymysql
import datetime
import uuid

def get_db_connection():
    """Establishes a database connection."""
    try:
        connection = pymysql.connect(
            host='licensedb.[region].rds.amazonaws.com',  # Replace with your database host
            user='licenseusr',  # Replace with your database username
            password='x4XtNHDJfPF8WWnhDQDmAUpn',  # Replace with your database password
            db='licensedb',  # Replace with your database name
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
