#!/usr/bin/env python

from flask import Response
import json


def get_created():
    """Return a generic 201 Created response"""
    js = {"status": "OK"}
    return Response(json.dumps(js), status=201, mimetype='application/json')


def get_user(user_data):
    del user_data['_id']
    del user_data['hash']

    return Response(
        json.dumps(user_data), status=201, mimetype='application/json')


def get_invalid_request():
    """Return when the user has made a bad request"""
    return get_json_error_response("Bad request format")


def get_user_exists():
    """Return when email or username is already taken"""
    return get_json_error_response("User already exists")


def get_json_error_response(message, code=400):
    data = {
        "error": message
    }
    js = json.dumps(data)

    return Response(js, status=code, mimetype='application/json')