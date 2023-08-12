#!/usr/bin/env python

from datetime import datetime
import json
import os

def read_config() -> dict:
    path_name = f"config.json"
    print(path_name)
    with open(path_name, "r") as f:
        return json.loads(f.read())

def get_datetime() -> dict:
    return {"timestamp": datetime.now().strftime("%Y%m%dT%H:%M:%S")}
