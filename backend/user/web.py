#!/usr/bin/env python

import flask
import users
import responses

app = flask.Flask(__name__)
LOGIN_PATH = '../../web/login'
SHARED_PATH = '../../web/shared'

@app.route('/')
def index():
    # If no session has been created
    return flask.redirect("/login")

# Requests for static resources
@app.route('/login')
def send_login():
    """Return the login page"""
    return flask.send_from_directory(LOGIN_PATH, 'index.html')

@app.route('/login/<path:path>')
def send_login_files(path):
    """Login page static resources - CSS, JS"""
    return flask.send_from_directory(LOGIN_PATH, path)

@app.route('/register')
def send_registrer():
    """Return the registration page"""
    return flask.send_from_directory(LOGIN_PATH, 'register.html')

@app.route('/forgotten-password')
def send_forgotten():
    """Return the forgotten password page"""
    return flask.send_from_directory(LOGIN_PATH, 'forgotten.html')

@app.route('/shared/<path:path>')
def send_shared_files(path):
    """Files used accross different web apps"""
    return flask.send_from_directory(SHARED_PATH, path)

# API Requests
@app.route('/signin', methods=['POST'])
def sign_in():
    """Request to authenticate with the system"""
    try:
        username_email = flask.request.form['username']
        password = flask.request.form['password']
    except:
        return responses.get_invalid_request()

    users.login(username_email, password)

@app.route('/signup', methods=['POST'])
def register():
    """Request to register with the system"""
    try:
        email = flask.request.form.email
        username = flask.request.form['username']
        display_name = flask.request.form['display-name']
        password = flask.request.form['password']
    except:
        return responses.get_invalid_request()

    users.register(username, email, password, display_name)

@app.route('/reset-password', methods=['POST'])
def reset_password():
    """Request to reset user password"""
    users.reset_password()

if __name__ == '__main__':
    app.run()
