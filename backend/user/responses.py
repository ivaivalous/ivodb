#!/usr/bin/env python

from flask import Response
import json

def get_invalid_request():
    """Return when the user has made a bad request"""
    data = {
        "error": "Bad request format"
    }
    js = json.dumps(data)

    return Response(js, status=400, mimetype='application/json')