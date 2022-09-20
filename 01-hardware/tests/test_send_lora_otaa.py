#! /usr/bin/env python3
# test: send join request to LoRaWAN TTN by OTAA identification
# version 1.0 - 23/11/21
# version 1.1 - 20/09/22 (change LoRaWAN import library)

import time, board
from time import sleep
from LoRaWAN import *
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from LoRaWAN.MHDR import MHDR
from random import randrange

BOARD.setup()

class LoRaWANotaa(LoRa):
    def __init__(self, verbose = True):
        super(LoRaWANotaa, self).__init__(verbose)
    
    def on_tx_done(self):
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        self.set_dio_mapping([0,0,0,0,0,0])
        self.set_invert_iq(1)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        print("TxDone")

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print("RxDone")

        lorawan = LoRaWAN.new([], appkey)
        lorawan.read(payload)
        print(lorawan.get_payload())
        print(lorawan.get_mhdr().get_mversion())

        if lorawan.get_mhdr().get_mtype() == MHDR.JOIN_ACCEPT:
            print("Got LoRaWAN join accept")
            print(lorawan.valid_mic())
            print(lorawan.get_devaddr())
            print(lorawan.derive_nwskey(devnonce))
            print(lorawan.derive_appskey(devnonce))
            print("\n")
            sys.exit(0)

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
lora = LoRaWANotaa(True)

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
