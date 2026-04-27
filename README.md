# 📚 Student Study Planner Management System

A full-stack web application for college students to manage subjects and study tasks.

**Stack:** Python (Flask) · MySQL · HTML/CSS/JS

---

## 🚀 Setup Instructions

### Step 1 – Install Python packages
```bash
pip install -r requirements.txt
```

### Step 2 – Set up MySQL Database
Open MySQL and run:
```bash
mysql -u root -p < database.sql
```
Or open MySQL Workbench / phpMyAdmin, create a new query, paste the contents of `database.sql`, and execute.

### Step 3 – Configure Database Credentials
Open `config.py` and update:
```python
DB_HOST = 'localhost'
DB_USER = 'root'        # your MySQL username
DB_PASSWORD = ''        # your MySQL password
DB_NAME = 'study_planner'
```

### Step 4 – Run the Application
```bash
python app.py
```

### Step 5 – Open in Browser
Visit: **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
study_planner/
├── app.py              # Main Flask app & all routes
├── config.py           # DB and secret key config
├── database.sql        # Database schema
├── requirements.txt    # Python dependencies
├── README.md           # This file
│
├── templates/          # HTML pages (Jinja2)
│   ├── base.html       # Shared layout with sidebar
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── subjects.html
│   ├── tasks.html
│   └── edit_task.html
│
├── static/
│   ├── css/style.css   # All styles
│   └── js/script.js    # Modal, search, filter logic
│
├── models/             # Database operations
│   ├── user_model.py
│   ├── subject_model.py
│   └── task_model.py
│
└── utils/
    ├── auth.py         # Login required decorator
    └── database.py     # MySQL connection helper
```

---

## ✨ Features

- 🔐 Secure login/register with password hashing (werkzeug)
- 📊 Dashboard with stats and progress bar
- 📖 Subject management (add/delete)
- ✅ Task management (add/edit/delete/toggle)
- 🔴 Overdue task highlighting
- 🔍 Live search and subject filter
- 📱 Responsive sidebar layout
- 💬 Flash messages for all actions

---

## 🔧 Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| DB connection error | Check `config.py` credentials |
| Port already in use | Change port: `app.run(port=5001)` |
| PRN already exists | Use a different PRN to register |
