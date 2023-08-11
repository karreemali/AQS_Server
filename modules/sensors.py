#!/usr/bin/env python

from abc import ABC

from utils import read_config, get_datetime

from pms5003 import PMS5003
import RPi.GPIO as GPIO
import dht11

class SetSensor(ABC):
    def read():
        pass

class ReadPMS5003(SetSensor):
    def __init__(self):
        self.sensor = PMS5003(
            device='/dev/ttyAMA0',
            baudrate=9600,
            pin_enable=22,
            pin_reset=27
        )
        self.output = {
        }

    def read(self) -> dict:
        data = self.sensor.read()
        return {"test": data.pm_ug_per_m3(2.5)}

class ReadDHT11(SetSensor):
    def __init__(self):
        self.sensor = 

    def read(self) -> dict:
        data = 


def read_sensors() -> dict:
    '''
    return all read sensor values. The sensors associated with the package is derived from the configs
    '''
    output = {}
    configs = read_config()
    sensors_on_package = configs.get("package_sensors", ["ReadPMS5003"])
    for sensor in sensors_on_package:
        output.update(sensor().read())
    output.update(get_datetime())
    return output
