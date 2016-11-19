#!/usr/bin/env python

import json

with open(path.join('config', 'config.json')) as config_file:    
    config = json.load(config_file)