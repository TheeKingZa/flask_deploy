#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/home')
def home():
    return render_template('home.html')


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
