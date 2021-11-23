#!/usr/bin/env python3

import sys
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
sys.path.insert(0, '/home/pi/solar_pi0_ws_otaa/04-lorawan')
from LoRaWAN.MHDR import MHDR
import adafruit_bmp3xx, board

BOARD.setup()
parser = LoRaArgumentParser("LoRaWAN sender")

class LoRaWANotaa(LoRa):
    def __init__(self, devaddr = [], nwkey = [], appkey = [], verbose = False):
        super(LoRaWANsend, self).__init__(verbose)
        self.devaddr = devaddr
        self.nwkey = nwkey
        self.appkey = appkey
    
    def on_tx_done(self):
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        print("TxDone")
        sys.exit(0)

def getPayloadMockBMP388():
    press_val = bmp.pressure
    temp_val = bmp.temperature + temperature_offset
    alt_val = bmp.altitude
    return encodePayload(press_val,temp_val,alt_val)

def encodePayload(pressure,temperature,altitude):
    # encode float as int
    press_val = int(pressure * 100) 
    temp_val = int(temperature * 100)
    alt_val = int(altitude * 100)
    abs_temp_val = abs(temp_val)

    # encode payload as bytes
    # pressure (needs 3 bytes)
    data[0] = (press_val >> 16) & 0xff
    data[1] = (press_val >> 8) & 0xff
    data[2] = press_val & 0xff

    # temperature (needs 3 bytes 327.67 max value) (signed int)
    if(temp_val < 0):
        data[3] = 1 & 0xff
    else:
        data[3] = 0 & 0xff
    data[4] = (abs_temp_val >> 8) & 0xff
    data[5] = abs_temp_val & 0xff

    # altitude (needs 3 bytes)
    data[6] = (alt_val >> 16) & 0xff
    data[7] = (alt_val >> 8) & 0xff
    data[8] = alt_val & 0xff

    return data

def sendDataTTN(data):
    lorawan = LoRaWAN.new(nwskey, appskey)
    lorawan.create(MHDR.UNCONF_DATA_UP, {'devaddr': devaddr, 'fcnt': 1, 'data': list(map(ord, data)) })

    self.write_payload(lorawan.to_raw(data))
    self.set_mode(MODE.TX)

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
i2c = board.I2C()   # uses board.SCL and board.SDA

# create library object using our Bus I2C port
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bmp.sea_level_pressure = 1013.25

bmp.pressure_oversampling = 1
bmp.temperature_oversampling = 1

# you will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5

for meas in range (0, 15, 1):
    packet = None
    sendDataTTN(getPayloadMockBMP388())
    print("packet sent!")
    time.sleep(2)
