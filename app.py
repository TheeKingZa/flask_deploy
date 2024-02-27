#!/usr/bin/env python3
from flask import (
  Flask,
  render_template,
  request,
  redirect,
  abort
)

# Create an instance of the Flask class
app = Flask(__name__)

# Define routes and their corresponding views
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<username>')
def show_user_profile(username):
    return f'User: {username}'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check username and password
        return 'Logged in successfully!'
    return render_template('login.html')


@app.route('/redirect')
def redirect_example():
    return redirect('/')

@app.route('/error')
def error_example():
    abort(404)


if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)
