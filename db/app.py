import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

# Specify the folder for templates. Because docker-compose mounts ./app to /app/templates,
# Flask will find your HTML files there.
app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Change for production

# Database file is stored in /app/data folder (shared volume)
DATABASE = os.path.join('data', 'users.db')

# Ensure that the data directory exists
os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                            (username, password)).fetchone()
        conn.close()
        if user:
            return redirect(url_for('welcome', username=username))
        else:
            message = "Invalid credentials. Please try again."
    return render_template('login.html', message=message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            message = "User exists"
        else:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('welcome', username=username))
        conn.close()
    return render_template('signup.html', message=message)

@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)

if __name__ == '__main__':
    # Bind to 0.0.0.0 so Docker can map the port correctly
    app.run(host='0.0.0.0', port=5000, debug=True)
