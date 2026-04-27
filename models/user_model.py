# ============================================
# models/user_model.py - User Database Operations
# ============================================

from utils.database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(name, prn, password):
    """Register a new user. Returns True if successful, False if PRN already exists."""
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed"
    try:
        cursor = conn.cursor()
        hashed_pw = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, prn, password) VALUES (%s, %s, %s)",
            (name, prn, hashed_pw)
        )
        conn.commit()
        return True, "Registration successful"
    except Exception as e:
        return False, f"PRN already exists or error: {e}"
    finally:
        cursor.close()
        conn.close()

def get_user_by_prn(prn):
    """Fetch a user record by PRN."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE prn = %s", (prn,))
        user = cursor.fetchone()
        return user
    finally:
        cursor.close()
        conn.close()

def verify_password(stored_hash, password):
    """Check if the given password matches the stored hash."""
    return check_password_hash(stored_hash, password)
