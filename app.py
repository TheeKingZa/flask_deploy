#!/usr/bin/env python3
from flask import (
    Flask,
    render_template,
    session,
    redirect,
    request,
    url_for,
    flash
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)
app.secret_key = 'admin'
UPLOAD_FOLDER = 'static/uploads/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Used for session encryption

# Path to the JSON database
db_path = 'data/users.json'

# Function to load users from JSON file
def load_users():
    if not os.path.exists(db_path):
        with open(db_path, 'w') as f:
            json.dump({}, f)
    with open(db_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

# Function to save users to JSON file
def save_users(users):
    with open(db_path, 'w') as f:
        json.dump(users, f, indent=2)
        
# Helper function to format names
def format_name(name):
    return name.capitalize()

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()

        if username not in users or not check_password_hash(users[username]['password'], password):
            return render_template('login.html', error='Invalid credentials')

        session['username'] = username  # Store the username in the session
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    # remove the username from session
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username'][:20] # only 20 characters
        first_name = format_name(request.form['first_name'])
        last_name = format_name(request.form['last_name'])
        email = request.form['email'].lower()
        cell_number = request.form['cell_number'][:10]
        dob = request.form['dob']
        id_number = request.form['id_number'][:13]
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Confirm password match
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        # Check password length
        if len(password) < 6:
            return render_template('signup.html', error='Password must be at least 6 characters long.')

        users = load_users()

        # Check for duplicate ID number(s)
        for user in users.values():
            if user['id_number'] == id_number:
                return render_template('signup.html', error='ID number already exists')

        # check for email duplicates
        for user in users.values():
            if user['email'] == email:
                return render_template('signup.html', error='E-mail already taken')


        # Hash the password
        hashed_password = generate_password_hash(password)

        users[username] = {
            'password': hashed_password,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'cell_number': cell_number,
            'dob': dob,
            'id_number': id_number,
            'profile_picture': None  # Initialize profile picture as None
        }
        save_users(users)
        session['username'] = username
        return redirect(url_for('home'))
    
    return render_template('signup.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    users = load_users()
    username = session['username']
    user = users.get(username, {})
    return render_template('profile.html', username=username, user=user)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' not in session:
        return redirect(url_for('login'))

    entered_username = request.form['username']
    session_username = session['username']

    if entered_username != session_username:
        return redirect(url_for('profile'))

    users = load_users()

    if session_username in users:
        del users[session_username]
        save_users(users)
        session.pop('username', None)  # Remove the username from the session
        return redirect(url_for('login'))

    return redirect(url_for('profile'))

@app.route('/upload_profile_picture', methods=['POST'])
def upload_profile_picture():
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'profile_picture' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('profile'))

    file = request.files['profile_picture']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('profile'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1].lower()
        username = session['username']
        filename = f"profile_picture.{extension}"
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
        os.makedirs(user_folder, exist_ok=True)
        filepath = os.path.join(user_folder, filename)
        file.save(filepath)

        # Update user's profile picture in the database
        users = load_users()
        if username in users:
            users[username]['profile_picture'] = os.path.join('uploads/profile_pics', username, filename)
            save_users(users)
        
        flash('Profile picture uploaded successfully!', 'success')
        return redirect(url_for('profile'))

    flash('Invalid file format', 'error')
    return redirect(url_for('profile'))


@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
