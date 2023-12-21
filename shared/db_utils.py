import pymysql
import json

def get_db_connection():
    """
    Creates a connection to the MariaDB database and returns the connection object.
    """
    try:
        connection = pymysql.connect(
            host='licensedb.[region].rds.amazonaws.com',  # Replace with your RDS endpoint
            user='licenseusr',                                       # Replace with your username
            password='x4XtNHDJfPF8WWnhDQDmAUpn',                           # Replace with your password
            db='licensedb',                                           # Replace with your database name
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MariaDB instance.")
        print(e)
        raise

def execute_query(sql, params=None, fetch_one=False):
    """
    Executes a given SQL query with optional parameters and returns the result.
    """
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        if fetch_one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
    connection.close()
    return result

def insert_record(sql, params):
    """
    Inserts a record into the database.
    """
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        connection.commit()
    connection.close()

# Additional utility functions can be added here
