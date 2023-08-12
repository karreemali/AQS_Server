#!/usr/bin/env python

from flask import Flask, render_template, request, jsonify
import os

from modules.sensors import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    '''
    healthcheck endpoint for flask
    '''
    return {"statusCode": 200}

@app.route('/sensors', methods=['GET'])
def sensors():
    '''
    initialize the package, then read all sensors within package
    return the data to the page
    '''
    package = read_sensors()
    return jsonify(package)
    #return """<html><meta http-equiv="refresh" content="30" />{}</html>""".format(data) # TODO: make content configurable


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
