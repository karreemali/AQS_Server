#!/usr/bin/env python

from abc import ABC
import inspect
import sys

from .utils import read_config, get_datetime

from pms5003 import PMS5003
# import RPi.GPIO as GPIO
import dht11
from sht_sensor import Sht, ShtVDDLevel
import mh_z19

EXISTING_CLASSES = ["read_sensors", "SetSensor"]
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
        return {
                "pm1l_0_3":data.pm_per_1l_air(0.3), 
                "pm1l_0_5":data.pm_per_1l_air(0.5), 
                "pm1l_1_0":data.pm_per_1l_air(1.0), 
                "pm1l_2_5":data.pm_per_1l_air(2.5),
                "pm1l_10":data.pm_per_1l_air(10)
                }

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

def check_classes(sensor_configs):
    '''
    gathers the class names and 
    '''
    class_names = [name for name, obj in inspect.getmembers(sys.modules[__name__])
                      if inspect.isclass(obj) and name not in EXISTING_CLASSES]
    
    class_classes = [obj for name, obj in inspect.getmembers(sys.modules[__name__])
                      if inspect.isclass(obj) and name not in EXISTING_CLASSES]
    
    select_classes = list(filter(lambda x: x[0] in sensor_configs, zip(class_names, class_classes)))
    return select_classes

def read_sensors() -> dict:
    '''
    return all read sensor values. The sensors associated with the package is derived from the configs
    '''
    output = CONFIGS.get("data", {})
    sensors_on_package = CONFIGS.get("package_sensors", ["ReadPMS5003"])
    get_sensors = check_classes(sensors_on_package)
    for sensor in get_sensors:
        output.update(sensor[1]().read())
    if CONFIGS.get("timestamp", None):
        output.update(get_datetime())
    return output
