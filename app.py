"""
Student Management System
Flask + SQLite CRUD Application
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os
import re
from functools import wraps
from math import ceil

app = Flask(__name__)
app.secret_key = 'sms_secret_key_2024_change_in_production'

DATABASE = 'database.db'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'
ITEMS_PER_PAGE = 8


# ─── Database Helpers ────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database and create tables."""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT    NOT NULL,
                email   TEXT    NOT NULL UNIQUE,
                mobile  TEXT    NOT NULL,
                course  TEXT    NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


# ─── Auth Decorator ──────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ─── Validation ──────────────────────────────────────────────────────────────

def validate_student(name, email, mobile, course):
    errors = []
    if not name or len(name.strip()) < 2:
        errors.append('Name must be at least 2 characters.')
    if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email):
        errors.append('Please enter a valid email address.')
    if not mobile or not re.match(r'^\+?[\d\s\-]{7,15}$', mobile):
        errors.append('Please enter a valid mobile number (7–15 digits).')
    if not course or len(course.strip()) < 2:
        errors.append('Course name must be at least 2 characters.')
    return errors


# ─── Auth Routes ─────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials. Try admin / admin123.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ─── Dashboard ───────────────────────────────────────────────────────────────

@app.route('/')
@login_required
def index():
    db = get_db()
    total   = db.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    courses = db.execute('SELECT COUNT(DISTINCT course) FROM students').fetchone()[0]
    recent  = db.execute('SELECT * FROM students ORDER BY id DESC LIMIT 5').fetchall()
    db.close()
    return render_template('index.html', total=total, courses=courses, recent=recent)


# ─── Students List ───────────────────────────────────────────────────────────

@app.route('/students')
@login_required
def students():
    query  = request.args.get('q', '').strip()
    page   = max(1, int(request.args.get('page', 1)))
    offset = (page - 1) * ITEMS_PER_PAGE

    db = get_db()
    if query:
        like = f'%{query}%'
        total_rows = db.execute(
            'SELECT COUNT(*) FROM students WHERE name LIKE ? OR email LIKE ? OR course LIKE ?',
            (like, like, like)
        ).fetchone()[0]
        rows = db.execute(
            'SELECT * FROM students WHERE name LIKE ? OR email LIKE ? OR course LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?',
            (like, like, like, ITEMS_PER_PAGE, offset)
        ).fetchall()
    else:
        total_rows = db.execute('SELECT COUNT(*) FROM students').fetchone()[0]
        rows = db.execute(
            'SELECT * FROM students ORDER BY id DESC LIMIT ? OFFSET ?',
            (ITEMS_PER_PAGE, offset)
        ).fetchall()
    db.close()

    total_pages = ceil(total_rows / ITEMS_PER_PAGE) if total_rows else 1
    return render_template('students.html',
                           students=rows,
                           query=query,
                           page=page,
                           total_pages=total_pages,
                           total_rows=total_rows)


# ─── Add Student ─────────────────────────────────────────────────────────────

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    courses = ['B.Tech', 'M.Tech', 'BCA', 'MCA', 'B.Sc', 'M.Sc',
               'B.Com', 'MBA', 'B.Arch', 'B.Pharm', 'Other']
    if request.method == 'POST':
        name   = request.form.get('name', '').strip()
        email  = request.form.get('email', '').strip().lower()
        mobile = request.form.get('mobile', '').strip()
        course = request.form.get('course', '').strip()

        errors = validate_student(name, email, mobile, course)
        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('add_student.html', courses=courses,
                                   name=name, email=email, mobile=mobile, course=course)
        try:
            with get_db() as conn:
                conn.execute(
                    'INSERT INTO students (name, email, mobile, course) VALUES (?, ?, ?, ?)',
                    (name, email, mobile, course)
                )
                conn.commit()
            flash(f'Student "{name}" added successfully!', 'success')
            return redirect(url_for('students'))
        except sqlite3.IntegrityError:
            flash('A student with this email already exists.', 'danger')

    return render_template('add_student.html', courses=courses,
                           name='', email='', mobile='', course='')


# ─── Edit Student ────────────────────────────────────────────────────────────

@app.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    courses = ['B.Tech', 'M.Tech', 'BCA', 'MCA', 'B.Sc', 'M.Sc',
               'B.Com', 'MBA', 'B.Arch', 'B.Pharm', 'Other']
    db = get_db()
    student = db.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    db.close()

    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('students'))

    if request.method == 'POST':
        name   = request.form.get('name', '').strip()
        email  = request.form.get('email', '').strip().lower()
        mobile = request.form.get('mobile', '').strip()
        course = request.form.get('course', '').strip()

        errors = validate_student(name, email, mobile, course)
        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('edit_student.html', student=student, courses=courses)
        try:
            with get_db() as conn:
                conn.execute(
                    'UPDATE students SET name=?, email=?, mobile=?, course=? WHERE id=?',
                    (name, email, mobile, course, student_id)
                )
                conn.commit()
            flash(f'Student "{name}" updated successfully!', 'success')
            return redirect(url_for('students'))
        except sqlite3.IntegrityError:
            flash('Another student with this email already exists.', 'danger')

    return render_template('edit_student.html', student=student, courses=courses)


# ─── Delete Student ──────────────────────────────────────────────────────────

@app.route('/students/delete/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    db = get_db()
    student = db.execute('SELECT name FROM students WHERE id = ?', (student_id,)).fetchone()
    db.close()
    if student:
        with get_db() as conn:
            conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
            conn.commit()
        flash(f'Student "{student["name"]}" deleted successfully.', 'success')
    else:
        flash('Student not found.', 'danger')
    return redirect(url_for('students'))


# ─── API: course stats for dashboard chart ───────────────────────────────────

@app.route('/api/course-stats')
@login_required
def course_stats():
    db = get_db()
    rows = db.execute(
        'SELECT course, COUNT(*) as count FROM students GROUP BY course ORDER BY count DESC'
    ).fetchall()
    db.close()
    return jsonify([{'course': r['course'], 'count': r['count']} for r in rows])


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
