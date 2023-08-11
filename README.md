# AQS_Server
Air Quality Sensor Flask application for PMS5003, S/DHT11, etc. Intended to be used with pub/sub or NoSQL DB.

## Overview
I got a bunch of these sensors lying around, and a bunch of Raspberry Pis, might as well make good use of them in a project!

1 DHT11, 1 PMS5003, Gas Monitor (Somewhere)
Future Me: CO2 Sensor (MH-Z19)

## Install
* Install all the prerequisite libs onto the host machine.
* Run the Flask App included in this repo
* Profit! (Caveat: Set up Prometheus prior to running)

Port by default is set to 5000, but I may make that configurable at a later point.

## Intent
The intent is to run the code on a Raspberry Pi Zero W for that ultra low profile form factor. Trying to push myself to finish some of these HA projects. 

I may want to run as a docker container for >Raspberry Pi 3.
