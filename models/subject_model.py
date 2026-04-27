# ============================================
# models/subject_model.py - Subject Operations
# ============================================

from utils.database import get_db_connection

def get_subjects(user_id):
    """Get all subjects belonging to a user."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM subjects WHERE user_id = %s ORDER BY subject_name",
            (user_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def add_subject(user_id, subject_name):
    """Add a new subject for the user."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO subjects (user_id, subject_name) VALUES (%s, %s)",
            (user_id, subject_name)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding subject: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_subject(subject_id, user_id):
    """Delete a subject (only if it belongs to the user)."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM subjects WHERE id = %s AND user_id = %s",
            (subject_id, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting subject: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
