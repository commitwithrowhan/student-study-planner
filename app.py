# ============================================
# app.py - Main Flask Application
# Student Study Planner
# ============================================

from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from utils.auth import login_required
from models.user_model import create_user, get_user_by_prn, verify_password
from models.subject_model import get_subjects, add_subject, delete_subject
from models.task_model import (get_tasks, get_task_by_id, add_task,
                                update_task, delete_task, toggle_task_status,
                                get_dashboard_stats)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/')
def index():
    """Redirect root to login page."""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show login form and handle login submission."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        prn = request.form.get('prn', '').strip()
        password = request.form.get('password', '')

        user = get_user_by_prn(prn)
        if user and verify_password(user['password'], password):
            # Save user info in session
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_prn'] = user['prn']
            flash('Welcome back, ' + user['name'] + '!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid PRN or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Show registration form and handle new user creation."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        prn = request.form.get('prn', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Basic validation
        if not name or not prn or not password:
            flash('All fields are required.', 'error')
        elif password != confirm:
            flash('Passwords do not match.', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
        else:
            success, msg = create_user(name, prn, password)
            if success:
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('PRN already registered. Try a different one.', 'error')

    return render_template('register.html')

@app.route('/logout')
def logout():
    """Clear session and redirect to login."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# ============================================
# DASHBOARD ROUTE
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Show main dashboard with stats and recent tasks."""
    stats = get_dashboard_stats(session['user_id'])
    return render_template('dashboard.html', stats=stats)

# ============================================
# SUBJECT ROUTES
# ============================================

@app.route('/subjects')
@login_required
def subjects():
    """Display all subjects for the logged-in user."""
    user_subjects = get_subjects(session['user_id'])
    return render_template('subjects.html', subjects=user_subjects)

@app.route('/add_subject', methods=['POST'])
@login_required
def add_subject_route():
    """Handle adding a new subject."""
    subject_name = request.form.get('subject_name', '').strip()
    if subject_name:
        add_subject(session['user_id'], subject_name)
        flash(f'Subject "{subject_name}" added successfully!', 'success')
    else:
        flash('Subject name cannot be empty.', 'error')
    return redirect(url_for('subjects'))

@app.route('/delete_subject/<int:subject_id>')
@login_required
def delete_subject_route(subject_id):
    """Delete a subject and all its tasks."""
    delete_subject(subject_id, session['user_id'])
    flash('Subject deleted successfully.', 'success')
    return redirect(url_for('subjects'))

# ============================================
# TASK ROUTES
# ============================================

@app.route('/tasks')
@login_required
def tasks():
    """Display all tasks with filter options."""
    user_tasks = get_tasks(session['user_id'])
    user_subjects = get_subjects(session['user_id'])
    return render_template('tasks.html', tasks=user_tasks, subjects=user_subjects)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task_route():
    """Handle adding a new task."""
    task_name = request.form.get('task_name', '').strip()
    subject_id = request.form.get('subject_id')
    deadline = request.form.get('deadline')

    if task_name and subject_id and deadline:
        add_task(session['user_id'], subject_id, task_name, deadline)
        flash('Task added successfully!', 'success')
    else:
        flash('All task fields are required.', 'error')
    return redirect(url_for('tasks'))

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task_route(task_id):
    """Show edit form and handle task update."""
    task = get_task_by_id(task_id, session['user_id'])
    if not task:
        flash('Task not found.', 'error')
        return redirect(url_for('tasks'))

    if request.method == 'POST':
        task_name = request.form.get('task_name', '').strip()
        subject_id = request.form.get('subject_id')
        deadline = request.form.get('deadline')
        status = request.form.get('status')

        update_task(task_id, session['user_id'], subject_id, task_name, deadline, status)
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks'))

    user_subjects = get_subjects(session['user_id'])
    return render_template('edit_task.html', task=task, subjects=user_subjects)

@app.route('/delete_task/<int:task_id>')
@login_required
def delete_task_route(task_id):
    """Delete a task."""
    delete_task(task_id, session['user_id'])
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('tasks'))

@app.route('/toggle_task/<int:task_id>')
@login_required
def toggle_task_route(task_id):
    """Toggle task status between Pending and Completed."""
    toggle_task_status(task_id, session['user_id'])
    return redirect(url_for('tasks'))

# ============================================
# RUN THE APP
# ============================================

if __name__ == '__main__':
    app.run(debug=True)
