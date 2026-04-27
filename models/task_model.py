# ============================================
# models/task_model.py - Task Operations
# ============================================

from utils.database import get_db_connection

def get_tasks(user_id):
    """Get all tasks for a user with subject names joined."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*, s.subject_name
            FROM tasks t
            JOIN subjects s ON t.subject_id = s.id
            WHERE t.user_id = %s
            ORDER BY t.deadline ASC
        """, (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def get_task_by_id(task_id, user_id):
    """Fetch a single task by ID (must belong to user)."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM tasks WHERE id = %s AND user_id = %s",
            (task_id, user_id)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def add_task(user_id, subject_id, task_name, deadline):
    """Add a new task."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (user_id, subject_id, task_name, deadline) VALUES (%s, %s, %s, %s)",
            (user_id, subject_id, task_name, deadline)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding task: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_task(task_id, user_id, subject_id, task_name, deadline, status):
    """Update an existing task."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET subject_id=%s, task_name=%s, deadline=%s, status=%s
            WHERE id=%s AND user_id=%s
        """, (subject_id, task_name, deadline, status, task_id, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating task: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_task(task_id, user_id):
    """Delete a task (only if it belongs to the user)."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s AND user_id = %s",
            (task_id, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting task: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def toggle_task_status(task_id, user_id):
    """Toggle task between Pending and Completed."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = IF(status='Pending','Completed','Pending') WHERE id=%s AND user_id=%s",
            (task_id, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error toggling task: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_dashboard_stats(user_id):
    """Fetch summary statistics for the dashboard."""
    conn = get_db_connection()
    if not conn:
        return {}
    try:
        cursor = conn.cursor(dictionary=True)

        # Count subjects
        cursor.execute("SELECT COUNT(*) as total FROM subjects WHERE user_id=%s", (user_id,))
        total_subjects = cursor.fetchone()['total']

        # Count all tasks
        cursor.execute("SELECT COUNT(*) as total FROM tasks WHERE user_id=%s", (user_id,))
        total_tasks = cursor.fetchone()['total']

        # Count completed
        cursor.execute("SELECT COUNT(*) as total FROM tasks WHERE user_id=%s AND status='Completed'", (user_id,))
        completed = cursor.fetchone()['total']

        # Recent 5 tasks
        cursor.execute("""
            SELECT t.*, s.subject_name FROM tasks t
            JOIN subjects s ON t.subject_id = s.id
            WHERE t.user_id=%s ORDER BY t.created_at DESC LIMIT 5
        """, (user_id,))
        recent_tasks = cursor.fetchall()

        return {
            'total_subjects': total_subjects,
            'total_tasks': total_tasks,
            'completed_tasks': completed,
            'pending_tasks': total_tasks - completed,
            'recent_tasks': recent_tasks
        }
    finally:
        cursor.close()
        conn.close()
