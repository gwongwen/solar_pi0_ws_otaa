#! /usr/bin/env python3
# test for bmp388 weather sensor 
# version 1.0 - 19/11/21
# version 1.1 - 25/11/21 (change while loop to for loop with 5 measures)

import time, busio, board, adafruit_bmp3xx
from busio import I2C
from time import sleep

# create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)       

# create library object using our Bus I2C port
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bmp.sea_level_pressure = 1013.25

# no IIR filter, no osr for lowest power (case of weather monitoring)
bmp.pressure_oversampling = 1
bmp.temperature_oversampling = 1

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5

for meas in range (0,5,1):
    print("\nTemperature: %0.1f C" % (bmp.temperature + temperature_offset))
    print("Pressure: %0.3f hPa" % bmp.pressure)
    print("Altitude: %0.2f meters" % bmp.altitude)
    time.sleep(1)

