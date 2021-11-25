#! /usr/bin/env python3
# test for parallel communication between sensor and radio bonnet i2c bus
# version 1.0 - 19/11/21

import time, busio, board, adafruit_ssd1306, adafruit_bmp3xx
from digitalio import DigitalInOut, Direction, Pull
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
from busio import I2C

# link buttons
btnA = DigitalInOut(board.D5) # Button A
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP
btnB = DigitalInOut(board.D6) # Button B
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP
btnC = DigitalInOut(board.D12) # Button C
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP
 
# create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# create library object using our Bus I2C port
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bmp.sea_level_pressure = 1013.25

bmp.pressure_oversampling = 1
bmp.temperature_oversampling = 1

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

# clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height
 
# TinyLoRa configuration
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

for meas in range (0,5,1):
    msg = ''
    msg += "Temperature: %0.1f C\n" % bmp.temperature + temperature_offset
    msg += "Pressure: %0.3f hPa\n" % bmp.pressure
    msg += "Altitude = %0.2f meters\n" % bmp.altitude

    display.fill(0)
    display.text(msg, 0, 0, 1)
    display.show()
    print(msg)

    time.sleep(1)