#!/usr/bin/env python

import flask
import requests
import re
import database
import responses
import scripter
import script_logger

from flask import request
from users import UserManager
from resources import ResourceManager
from security import Jwt


LOGIN_PATH = '../../web/login'
SHARED_PATH = '../../web/shared'
CP_PATH = '../../web/cp'
ALLOWED_METHODS = ['GET', 'PUT', 'POST', 'PATCH']
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
        valid, user_info = Jwt().validate_jwt(flask.request.cookies['jwt'])
        user_id = user_info['_id']
        user_name = user_info['username']

    if valid:
        resources = ResourceManager(db).get_resources(user_id)
        # TODO move cp.html from the login folder
        return flask.render_template(
            'cp.html', resources=resources, user_name=user_name)

    return flask.redirect("/login")


@app.route('/cp/<path:path>')
def send_ucp_files(path):
    """User CP page static resources - CSS, JS"""
    if 'jwt' in flask.request.cookies:
        if Jwt().validate_jwt(flask.request.cookies['jwt']):
            return flask.send_from_directory(CP_PATH, path)

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
        r_type = flask.request.form['type']
        body = flask.request.form['body']
        headers = flask.request.form['headers']
    except:
        return responses.get_invalid_request()

    ResourceManager(db).create(user_id, name, path, r_type, body, headers)
    return responses.get_created()


# Make a resource inactive - it will no longer be publicly visible
@app.route('/deactivate', methods=['POST'])
def deactivate_resource():
    valid = False

    if 'jwt' in flask.request.cookies:
        valid, user_info = Jwt().validate_jwt(flask.request.cookies['jwt'])

    if not valid:
        return responses.get_json_error_response("Bad login")

    try:
        user_id = user_info['_id']
        path = flask.request.form['path']
    except:
        return responses.get_invalid_request()

    ResourceManager(db).deactivate(user_id, path)
    return responses.get_created()


# Make a resource inactive - it will no longer be publicly visible
@app.route('/activate', methods=['POST'])
def activate_resource():
    valid = False

    if 'jwt' in flask.request.cookies:
        valid, user_info = Jwt().validate_jwt(flask.request.cookies['jwt'])

    if not valid:
        return responses.get_json_error_response("Bad login")

    try:
        user_id = user_info['_id']
        path = flask.request.form['path']
    except:
        return responses.get_invalid_request()

    ResourceManager(db).activate(user_id, path)
    return responses.get_created()


# Permanently delete a resource
@app.route('/delete/<resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    valid = False

    if 'jwt' in flask.request.cookies:
        valid, user_info = Jwt().validate_jwt(flask.request.cookies['jwt'])

    if not valid:
        return responses.get_json_error_response("Bad login")

    try:
        user_id = user_info['_id']
    except:
        return responses.get_invalid_request()

    ResourceManager(db).delete(user_id, resource_id)
    return responses.get_created()


# Get a resource body
# TODO migrate to the consumer app
@app.route(
    '/u/<user_name>/<path>',
    defaults={'params': ''},
    methods=ALLOWED_METHODS)
@app.route('/u/<user_name>/<path>/<params>', methods=ALLOWED_METHODS)
def load_resource(user_name, path, params):
    body, headers, r_type = ResourceManager(db).get_resource_for_display(
        user_name, path)
    
    if body is None:
        return flask.render_template('404.html')

    if r_type == "proxy":
        resp = get_proxy_response(request, body, params)
    elif r_type == "script":
        resp, logs = scr.run(request, body, params)
        scr_logger.save(user_name, path, logs)
    else:
        resp = flask.Response(body)

    # Set pre-configured headers
    for key, value in headers.iteritems():
        resp.headers[key] = value

    return resp

@app.route('/u/<user_name>/logs/<path>', methods=["GET"])
def get_logs(user_name, path):
    logs = scr_logger.load(user_name, path)
    resp = flask.Response(logs)
    return resp

# TODO: Move away
def get_proxy_response(request, target_url, url_params):
    request_headers = {}
    url = target_url + '/' + url_params

    print(url)

    for key, value in request.headers:
        if key == 'Host':
            continue
        request_headers[key] = value

    resp = requests.request(
        method=request.method,
        url=url,
        headers=request_headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = [
        'content-encoding', 'content-length',
        'transfer-encoding', 'connection',
        'cookie'
    ]

    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = flask.Response(resp.content, resp.status_code, headers)
    return response


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
    scr = scripter.Scripter()
    scr_logger = script_logger.ScriptLogger(db)
    app.run()
