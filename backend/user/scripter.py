#!/usr/bin/env python

from selenium import webdriver

class Scripter():

    # This file contains/references the default JS
    # used to provide functions dealing with input/output
    SCRIPT_RUNNER = "runner.html"

    def __init__(self):
        pass

    @staticmethod
    def run(request, script_body, input_params):
        driver = webdriver.PhantomJS()
        driver.get(SCRIPT_RUNNER)
        driver.execute_script(
            build_runner_sript(request, input_params))
        
        return driver.execute_script(script_body)

    @staticmethod
    def build_runner_sript(request, input_params):
        # Build JS related to having access to input
        # and request data.
        pass