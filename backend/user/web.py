#!/usr/bin/env python

import flask
import database
import responses
from users import UserManager
from resources import ResourceManager
from security import Jwt


LOGIN_PATH = '../../web/login'
SHARED_PATH = '../../web/shared'
CP_PATH = '../../web/cp'
app = flask.Flask(__name__, template_folder=LOGIN_PATH)


@app.route('/')
def index():
    # If no session has been created
    return flask.redirect("/login")


# Requests for static resources
@app.route('/login')
def send_login():
    """Return the login page"""
    valid = False

    if 'jwt' in flask.request.cookies:
        valid = Jwt().validate_jwt(flask.request.cookies['jwt'])

    if valid:
        return flask.redirect('/cp')

    return flask.render_template('index.html')


@app.route('/login/<path:path>')
def send_login_files(path):
    """Login page static resources - CSS, JS"""
    return flask.send_from_directory(LOGIN_PATH, path)


@app.route('/register')
def send_register():
    """Return the registration page"""
    return flask.render_template('register.html')


@app.route('/cp')
def user_cp():
    """Return the user control panel app"""
    valid = False

    if 'jwt' in flask.request.cookies:
        valid = Jwt().validate_jwt(flask.request.cookies['jwt'])

    if valid:
        return flask.send_from_directory(CP_PATH, 'index.html')
    return flask.redirect("/login")


# Create a new resource
@app.route('/new', methods=['POST'])
def create_resource():
    valid = False

    if 'jwt' in flask.request.cookies:
        valid, user_info = Jwt().validate_jwt(flask.request.cookies['jwt'])

    if not valid:
        return responses.get_json_error_response("Bad login")

    try:
        user_id = user_info['_id']
        name = flask.request.form['name']
        path = flask.request.form['path']
        body = flask.request.form['body']
    except:
        return responses.get_invalid_request()

    ResourceManager(db).create(user_id, name, path, body)
    return responses.get_created()


# Get a resource body
# TODO migrate to the consumer app
@app.route('/u/<user_name>/<path>')
def load_resource(user_name, path):
    body = ResourceManager(db).get_resource_body(user_name, path)
    
    if body is None:
        return flask.render_template('404.html')
    return body


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

    try:
        user, jwt = UserManager(db).login(username_email, password)
    except:
        # TODO probably use a redirect instead of rendering
        return flask.render_template('index.html', login_error=True)

    response = flask.make_response(flask.redirect('/cp'))
    response.set_cookie('jwt', jwt)
    return response


@app.route('/signup', methods=['POST'])
def register():
    """Request to register with the system"""
    try:
        email = flask.request.form['email']
        username = flask.request.form['username']
        display_name = flask.request.form['display-name']
        password = flask.request.form['password']
    except:
        return responses.get_invalid_request()

    try:
        UserManager(db).register(username, email, password, display_name)
        return flask.render_template('register.html', success=True)
    except:
        # Such user already existed
        return flask.render_template(
            'register.html',
            success=False,
            email=email, username=username,
            display_name=display_name)


@app.route('/reset-password', methods=['POST'])
def reset_password():
    """Request to reset user password"""
    UserManager(db).reset_password()


if __name__ == '__main__':
    db = database.Database()
    app.run()
