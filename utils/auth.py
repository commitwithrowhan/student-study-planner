# ============================================
# utils/auth.py - Authentication Helper
# ============================================

from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    """
    Decorator to protect routes that require login.
    Usage: @login_required above any route function.
    Redirects to login page if user is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
