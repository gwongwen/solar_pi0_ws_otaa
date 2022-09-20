#! /usr/bin/env python3
# test for rfm9x chipset radio
# version 1.0 - 19/11/21
# version 1.1 - 20/07/22 (add a send packet code)
# version 1.2 - 20//09/22 (add RFM9x configurations for tests)

import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board

# import the SSD1306 module.
import adafruit_ssd1306
# import the RFM9x radio module.
import adafruit_rfm9x

# button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

# clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# attempt to set up the RFM9x Module
try: 
    # initialize RFM radio
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.1)
    display.text('RFM9x: Detected', 0, 0, 1)
except RuntimeError as error:
     # thrown on version mismatch
    display.text('RFM9x: ERROR', 0, 0, 1)
    print('RFM9x Error: ', error)
display.show()

# Apply new modem config settings to the radio to improve its effective range
rfm9x.signal_bandwidth = 62500
rfm9x.coding_rate = 4/5
rfm9x.spreading_factor = 8
rfm9x.enable_crc = True

while True:
    # clear the image
    display.fill(0)

    # send a packet
    rfm9x.send(bytes("Hello World!\r\n","utf-8"))
    print("Sent Hello World message!")

    # check buttons
    if not btnA.value:
        # button A pressed
        display.text('Ada', width-85, height-7, 1)
        display.show()
        time.sleep(0.1)
    if not btnB.value:
        # button B pressed
        display.text('Fruit', width-75, height-7, 1)
        display.show()
        time.sleep(0.1)
    if not btnC.value:
        # button C pressed
        display.text('Radio', width-65, height-7, 1)
        display.show()
        time.sleep(0.1)

    display.show()
    time.sleep(0.1)