# database.py
import pymysql

def get_db_connection():
    db = pymysql.connect(
        host='localhost',
        user='your_db_user',          # Replace with your actual DB user
        password='your_actual_password',  # Replace with your actual password
        database='user_identification' # Replace with your actual database name
    )
    return db
