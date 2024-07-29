import sqlite3
import jwt
import datetime
import smtplib
from email.mime.text import MIMEText

DATABASE = 'login.db'
SECRET_KEY = 'f3409b3ed086f6b5756574730a00590a'

# Predefined admin credentials
ADMIN_EMAIL = "samnjorokibandi@gmail.com"
ADMIN_PASSWORD = "samnjoro@2030"

def initialize_login_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def send_reset_email(email, reset_token):
    msg = MIMEText(f"Click the link to reset your password: http://localhost:5000/reset-password?token={reset_token}")
    msg['Subject'] = 'Password Reset'
    msg['From'] = 'samnjorokibandi@gmail.com'
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('samnjorokibandi@gmail.com', 'email password')
        server.sendmail('samnjorokibandi@gmail.com', email, msg.as_string())

def add_admin_user():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)', (ADMIN_EMAIL, ADMIN_PASSWORD))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY)
        return True, token
    return False, 'Invalid credentials'

def get_user_by_email(email):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

# Initialize the database and add the admin user
initialize_login_db()
add_admin_user()