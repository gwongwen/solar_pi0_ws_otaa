#! /usr/bin/env python3
# test: send physical data from sensor to LoRaWAN TTN by OTAA identification
# version 1.0 - 23/11/21

import time, board, LoRaWAN
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
from LoRaWAN.MHDR import MHDR
from random import randrange

BOARD.setup()
parser = LoRaArgumentParser("LoRaWAN sender")

class LoRaWANotaa(LoRa):
    def __init__(verbose = False):
        super(LoRaWANotaa, self).__init__(verbose)
    
    def on_tx_done(self):
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        print("TxDone")

    def start(self):
        self.tx_counter = 1
        lorawan = LoRaWAN.new(appkey)
        lorawan.create(MHDR.JOIN_REQUEST, {'deveui': deveui, 'appeui': appeui, 'devnonce': devnonce})
        self.write_payload(lorawan.to_raw())
        self.set_mode(MODE.TX)
        while True:
            sleep(1)
            
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
lora.set_spreading_factor(9)
lora.set_pa_config(max_power=0x0F, output_power=0x0E)
lora.set_sync_word(0x34)
lora.set_rx_crc(True)

print(lora)
assert(lora.get_agc_auto_on() == 1)

try:
    print("Sending LoRaWAN join request\n")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("\nKeyboardInterrupt")
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
