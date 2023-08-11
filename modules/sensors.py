#!/usr/bin/env python

from abc import ABC

from utils import read_config, get_datetime

from pms5003 import PMS5003
# import RPi.GPIO as GPIO
import dht11
from sht_sensor import Sht, ShtVDDLevel
import mh_z19

CONFIGS = read_config()

class SetSensor(ABC):
    def read(self):
        pass

class ReadPMS5003(SetSensor):
    '''
    Particulate matter sensor
    '''
    def __init__(self):
        self.sensor = PMS5003(
            device='/dev/ttyAMA0',
            baudrate=9600,
            pin_enable=22,
            pin_reset=27
        )

    def read(self) -> dict:
        data = self.sensor.read()
        return {"test": data.pm_ug_per_m3(2.5)}

class ReadDHT11(SetSensor):
    '''
    Temp/Humidity sensor
    '''
    def __init__(self):
        self.sensor = dht11.DHT11(pin=14) #TODO replace with configurable
    def read(self) -> dict:
        data = {
            "dht11_temp": self.sensor.temperature,
            "dht11_hum": self.sensor.humidity,
        }
        return data

class ReadSHT(SetSensor):
    '''
    Temp/Humidity sensor
    '''
    def __init__(self):
        self.sensor = Sht(21, 17, voltage=ShtVDDLevel.vdd_5v) #TODO: Configurable
    def read(self):
        _t = self.sensor.read_t()
        _rh = self.sensor.read_rh(_t)
        _dp = self.sensor.read_dew_point(_t, _rh)
        data = {
            "sht_temp": _t,
            "sht_hum": _rh,
            "sht_dew_point": _dp
        }
        return data

class ReadMHZ19(SetSensor):
    '''
    CO2 Concentration Sensor
    '''
    def __init__(self):
        self.sensor = mh_z19.read_all()
    def read(self):
        data = {}
        for k, v in self.sensor.items():
            data[f"mh_z19_{k}"] = v
        return data

def read_sensors() -> dict:
    '''
    return all read sensor values. The sensors associated with the package is derived from the configs
    '''
    output = {}
    sensors_on_package = CONFIGS.get("package_sensors", ["ReadPMS5003"])
    for sensor in sensors_on_package:
        output.update(sensor().read())
    if CONFIGS.get("timestamp", None):
        output.update(get_datetime())
    return output
