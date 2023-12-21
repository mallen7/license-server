import json
import pymysql
import datetime

def log_event(function_name, event_type, message, additional_info=None):
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
