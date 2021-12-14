#! /usr/bin/env python3
# run: send physical data from sensor to LoRaWAN TTN by OTAA identification
# version 1.1 - 14/12/21

import time, busio, board, adafruit_bmp3xx, LoRaWAN
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
from LoRaWAN.MHDR import MHDR
from busio import I2C
from random import randrange
from time import sleep


BOARD.setup()
parser = LoRaArgumentParser("LoRaWAN sender")

class LoRaWANotaa(LoRa):
    def __init__(self, verbose = False):
        super(LoRaWANotaa, self).__init__(verbose)
    
    def on_tx_done(self):
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        print("TxDone")

    def start(self):
        self.tx_counter = 1
        lorawan = LoRaWAN.new(appkey)
        lorawan.create(MHDR.JOIN_REQUEST, {'deveui': deveui, 'appeui': appeui, 'devnonce': devnonce, 'data':list(meas)})
        self.write_payload(lorawan.to_raw())
        self.set_mode(MODE.TX)

def bmp388_payload():
    pressure = bmp.pressure
    temperature = bmp.temperature + temperature_offset

    # encode float as int
    press_val = int(pressure * 100) 
    temp_val = int(temperature * 100)
    abs_temp_val = abs(temp_val)

    # encode payload as bytes
    # pressure (needs 2 bytes)
    data[0] = (press_val >> 8) & 0xff
    data[1] = press_val & 0xff

    # temperature (needs 3 bytes 327.67 max value) (signed int)
    if(temp_val < 0):
        data[2] = 1 & 0xff
    else:
        data[2] = 0 & 0xff
    data[3] = (abs_temp_val >> 8) & 0xff
    data[4] = abs_temp_val & 0xff

    return data

# init
deveui = [0x00, 0x47, 0x64, 0xB1, 0xAB, 0xC6, 0x4F, 0x7C]
appeui = [0x70, 0xB3, 0xD5, 0x7E, 0xF0, 0x00, 0x51, 0x34]
appkey = [ 0x4A, 0xD7, 0xB6, 0x3F, 0x86, 0xAB, 0xC7, 0x54, 0xCF, 0x26, 0x8E, 0xE5, 0x60, 0xDE, 0x1C, 0x99]
devnonce = [randrange(256), randrange(256)]
lora = LoRaWANotaa(False)

# setup
lora.set_mode(MODE.SLEEP)
lora.set_dio_mapping([1,0,0,0,0,0])
lora.set_freq(868.1)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(7)
lora.set_pa_config(max_power=0x0F, output_power=0x0E)
lora.set_sync_word(0x34)
lora.set_rx_crc(True)

# create the i2c interface
i2c = busio.I2C(board.SCL, board.SDA)   # uses board.SCL and board.SDA

# create library object using our Bus I2C port
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bmp.sea_level_pressure = 1013.25

# no IIR filter, no osr for lowest power (case of weather monitoring)
bmp.pressure_oversampling = 1
bmp.temperature_oversampling = 1

# calibration of temperature sensor
temperature_offset = -5

# 2b array to store sensor data
data = bytearray(5)

for ind in range (0, 15, 1):
    meas = bmp388_payload()
    lora.start()
