# EduTrack — Student Management System

A modern, full-stack Student Management System built with Python Flask + SQLite.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher installed
- pip (Python package manager)

### 2. Install Dependencies
```bash
pip install flask
```

### 3. Run the Application
```bash
cd student_management
python app.py
```

### 4. Open in Browser
```
http://127.0.0.1:5000
```

### 5. Login Credentials
| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `admin123` |

---

## 📁 Project Structure

```
student_management/
├── app.py                  # Main Flask application
├── database.db             # SQLite database (auto-created)
├── requirements.txt        # Python dependencies
├── templates/
│   ├── base.html           # Base layout (sidebar + topbar)
│   ├── login.html          # Login page
│   ├── index.html          # Dashboard with stats & chart
│   ├── students.html       # Student list with search & pagination
│   ├── add_student.html    # Add student form
│   └── edit_student.html   # Edit student form
└── static/
    ├── css/style.css       # Full custom design system
    └── js/main.js          # Interactivity (sidebar, alerts)
```

---

## ✨ Features

- **Dashboard** — Total count, course distribution chart, recent enrollments
- **CRUD** — Add, View, Edit, Delete students
- **Search** — Filter by name, email, or course
- **Pagination** — 8 students per page
- **Validation** — Server-side field & email validation
- **Flash Messages** — Auto-dismissing success/error alerts
- **Login/Logout** — Session-based admin authentication
- **Responsive** — Mobile + desktop ready

---

## 🗄 Database Schema

```sql
CREATE TABLE students (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    email      TEXT    NOT NULL UNIQUE,
    mobile     TEXT    NOT NULL,
    course     TEXT    NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 Configuration

Edit these constants in `app.py` to customize:

```python
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'  # Change for production!
ITEMS_PER_PAGE = 8
```

---

## 🎨 Tech Stack

| Layer     | Technology               |
|-----------|--------------------------|
| Backend   | Python 3, Flask          |
| Database  | SQLite (built-in)        |
| Frontend  | Bootstrap 5 + Custom CSS |
| Fonts     | Syne + DM Sans (Google)  |
| Charts    | Chart.js                 |
| Icons     | Bootstrap Icons          |
