#!/usr/bin/env python

from flask import Flask, send_from_directory, redirect

app = Flask(__name__)
LOGIN_PATH = '../../web/login'
SHARED_PATH = '../../web/shared'

@app.route('/')
def index():
    # If no session has been created
    return redirect("/login")

# Requests for static resources
@app.route('/login')
def send_login():
    """Return the login page"""
    return send_from_directory(LOGIN_PATH, 'index.html')

@app.route('/login/<path:path>')
def send_login_files(path):
    """Login page static resources - CSS, JS"""
    return send_from_directory(LOGIN_PATH, path)

@app.route('/register')
def send_registrer():
    """Return the registration page"""
    return send_from_directory(LOGIN_PATH, 'register.html')

@app.route('/shared/<path:path>')
def send_shared_files(path):
    """Files used accross different web apps"""
    return send_from_directory(SHARED_PATH, path)

# API Requests
@app.route('/signin')
def sign_in():
    """Request to authenticate with the system"""
    pass

@app.route('/register')
def register():
    """Request to register with the system"""
    pass

if __name__ == '__main__':
    app.run()
