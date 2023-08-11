#!/usr/bin/env python

from datetime import datetime
import json

def read_config():
    with open("../config.json", "r") as f:
        return json.load(f.read())

def get_datetime():
    return datetime.now().strftime("%Y%m%dT%H:%M:%S")
