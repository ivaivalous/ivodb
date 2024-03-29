#!/usr/bin/env python

import responses
from selenium import webdriver

# This file contains/references the default JS
# used to provide functions dealing with input/output
SCRIPT_RUNNER = "runner.html"
ENCODING = 'utf-8'

PAGE_LOAD_TIMEOUT = 5
PAGE_LOAD_TIMEOUT_MS = PAGE_LOAD_TIMEOUT * 1000

capabilities = webdriver.DesiredCapabilities.PHANTOMJS
capabilities["phantomjs.page.settings.resourceTimeout"] = PAGE_LOAD_TIMEOUT_MS
capabilities["phantomjs.page.settings.loadImages"] = False

SCRIPT_TEMPLATE = """
    window.requestData = {{method:"{0}", headers:{1}, data:"{2}", params:{3}}};
    window.method = requestData.method;
    window.headers = requestData.headers;
    window.data = requestData.data;
    window.params = requestData.params;
    window.logs = [];
    window.log = function(message) {{
        window.logs.push({{
            "time": (new Date).getTime(),
            "message": message
        }})
    }};
"""
GET_LOGS_SCRIPT = 'return window.logs;'


class Scripter:
    def __init__(self):

        self.driver = webdriver.PhantomJS(desired_capabilities=capabilities)
        self.driver.implicitly_wait(PAGE_LOAD_TIMEOUT)
        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    def run(self, request, script_body, input_params):
        self.driver.get(SCRIPT_RUNNER)
        self.driver.execute_script(
            Scripter.build_runner_script(request, input_params))
        
        try:
            response = self.execute_user_script(script_body)
            logs = self.driver.execute_script(GET_LOGS_SCRIPT)
            return response.encode(ENCODING), logs
        except:
            return responses.get_invalid_request(), []

    def execute_user_script(self, script_body):
        """Execute a user-contributed script."""
        return self.driver.execute_script(script_body)

    @staticmethod
    def build_runner_script(request, input_params):
        # Build JS related to having access to input
        # and request data.
        return SCRIPT_TEMPLATE.format(
            request.method,
            Scripter.build_headers_map(request.headers),
            request.get_data().encode(ENCODING),
            Scripter.build_params_map(input_params.encode(ENCODING)))

    @staticmethod
    def build_params_map(input_params):
        # input_params looks like "test=aaa&test2=jjj"
        couples = input_params.split("&")
        params_map = {}

        for couple in couples:
            c = couple.split("=")
            key = c[0]
            value = c[1] if len(c) > 1 else ""
            params_map[key] = value

        return params_map

    @staticmethod
    def build_headers_map(headers):
        headers_map = {}

        for key, value in headers:
            if 'jwt=' in value:
                continue
            headers_map[key] = value.encode(ENCODING)

        return headers_map
