#!/usr/bin/env python

from flask import Flask, render_template, request, jsonify
import logging
from logging import Formatter, FileHandler
from forms import *
import os

from modules.sensors import *


@app.route('/')
def home():
    '''
    healthcheck endpoint for flask
    '''
    return "SUCCESS"

@app.route('/sensors')
def sensors():
    '''
    initialize the package, then read all sensors within package
    '''
    package = read_sensors()
    return jsonify(package)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
