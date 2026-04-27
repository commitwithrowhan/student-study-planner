# ============================================
# utils/database.py - Database Connection
# ============================================

import mysql.connector
from config import Config

def get_db_connection():
    """
    Creates and returns a new MySQL database connection.
    Call this at the start of each route that needs DB access.
    """
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None
