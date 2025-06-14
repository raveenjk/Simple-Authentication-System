from flask import Flask, request, render_template, redirect, url_for, flash, make_response
import sqlite3
import hashlib
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'simple_secret_key'  # In production, use a strong, random key

# JWT configuration
JWT_SECRET = app.secret_key
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_MINUTES = 30

# Database initialization
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# JWT helper functions
def create_token(username):
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        
        if not token:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.username = data['username']
        except jwt.ExpiredSignatureError:
            flash('Session expired. Please log in again', 'error')
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            flash('Invalid session. Please log in again', 'error')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('register.html')
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                          (username, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'error')
            return render_template('register.html')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        # Hash the password for comparison
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE username = ? AND password = ?', 
                      (username, hashed_password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            token = create_token(username)
            response = make_response(redirect(url_for('protected')))
            response.set_cookie('token', token, httponly=True)
            flash('Login successful', 'success')
            return response
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/protected')
@token_required
def protected():
    return render_template('protected.html', username=request.username)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    response.set_cookie('token', '', expires=0)
    flash('You have been logged out', 'success')
    return response

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=3000)