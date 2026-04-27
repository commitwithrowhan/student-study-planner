# ============================================
# config.py - Application Configuration
# ============================================

class Config:
    # Flask secret key for session encryption
    # CHANGE THIS to a long random string in production!
    SECRET_KEY = 'study_planner_secret_key_change_in_production'

    # MySQL Database Configuration
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_USER = 'root'         # Change to your MySQL username
    DB_PASSWORD = 'Akyu@6069s'         # Change to your MySQL password
    DB_NAME = 'study_planner'
