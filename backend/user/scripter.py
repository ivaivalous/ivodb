#!/usr/bin/env python

import responses
from selenium import webdriver

# This file contains/references the default JS
# used to provide functions dealing with input/output
SCRIPT_RUNNER = "runner.html"
ENCODING = 'utf-8'

class Scripter():

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def run(self, request, script_body, input_params):
        self.driver.get(SCRIPT_RUNNER)
        self.driver.execute_script(
            Scripter.build_runner_sript(request, input_params))
        
        try:
            response = self.driver.execute_script(script_body)
            return response.encode('utf-8')
        except:
            return responses.get_invalid_request()

    @staticmethod
    def build_runner_sript(request, input_params):
        # Build JS related to having access to input
        # and request data.
        print(request.method)
        fmt = (
            'window.requestData ='
            '    {{method:"{0}",data:"{1}",params:"{2}"}}')

        return fmt.format(
            request.method,
            request.get_data().encode(ENCODING),
            input_params.encode(ENCODING))