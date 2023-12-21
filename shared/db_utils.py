import pymysql

def get_db_connection():
    """
    Creates a connection to the MariaDB database and returns the connection object.
    Make sure to replace the placeholders with your actual database details.
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
