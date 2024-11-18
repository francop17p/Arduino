# Data Acquisition Service

A python script that groups data from multiple sources and send it through MQTT protocol for Real-Time service. Script was used and tested on a Raspberry Pi 5.

## Features
- Reads data from an Arduino:
  - Temperature (°C)
  - Humidity (%)
  - Light intensity (units)

## Prerequisites
- Python 3.7 or higher
- Arduino with sensors:
  - DHT11 (Temperature & Humidity)
  - Photoresistor (Light)
