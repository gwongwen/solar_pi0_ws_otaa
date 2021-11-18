from dotenv import load_dotenv
import threading, time, subprocess, busio, board, adafruit_ssd1306, adafruit_bmp3xx, os, sys, random
from digitalio import DigitalInOut, Direction, Pull
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
from pathlib import Path

# updates the sleep time on the environment and on the 
# .env.dynamic file
# PARAMS: 
# - env-file: name of the file in which update the time value
# - value: new sleep time value
# ATENTION: this method will crush the env_file and create another one
# containing only that line
#
# RETURN: None
def setNewSleepTime(env_file, value):
    dynamic_env_file = open(env_file, "w")
    dynamic_env_file.write("export SLEEPTIME = "+str(value))
    dynamic_env_file.close()
    os.environ[key] = value

# get the TTN key from the env and pass it to bytearray
# PARAMS: 
# - key: key needed (must be on the .env file) 
# RETURN: bytearray key value     
def getTTNKey(key):
    try:
        key_to_retrieve_string = os.getenv(key)
        key_to_retrieve_bytearray = bytearray.fromhex(key_to_retrieve_string)
        return key_to_retrieve_bytearray
    except Exception:
        print("Error retrieving TTN key")
        print(sys.exc_info())
        sys.exit()

# get the TTN country code as an string
# PARAMS: None
# RETURN: string country code value 
def getTTNCountryFromENV():
    try:
        country = os.getenv("COUNTRY")
        return country
    except Exception:
        print("Error retrieving TTN country code")
        print(sys.exc_info())
        sys.exit()

def loadEnv(env_file_name):
    try:
        env_path = Path('.') / env_file_name
        load_dotenv(dotenv_path=env_path)
    except Exception:
        print("Couldnt load ENV")
        print(sys.exc_info())
        sys.exit()

# generate fake data body
# PARAMS: None
# RETURN: data encoded
def getPayloadMockBMP388():
    press_val = bmp.pressure
    temp_val = bmp.temperature + temperature_offset
    alt_val = bmp.altitude
    return encodePayload(press_val,temp_val,alt_val)

# encodes payload
# PARAMS: pressure, temperature, and altitude from BME388 sensor
# RETURN: data encoded
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

# send data
# PARAMS: data
# RETURN: None
def sendDataTTN(data):
    lora.send_data(data, len(data), lora.frame_counter)
    lora.frame_counter += 1
    display.fill(0)
    display.text('Packet sent', 10, 0, 1)
    display.show()

# init env 
loadEnv('.env')
loadEnv('.env.dynamic')

# link buttons
btnA = DigitalInOut(board.D5) # button A
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP
btnB = DigitalInOut(board.D6) # button B
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP
btnC = DigitalInOut(board.D12) # button C
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP
 
# create the i2c interface
i2c = board.I2C()   # uses board.SCL and board.SDA
 
# 128x32 OLED display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)

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

# clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height
 
# TinyLoRa configuration
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.CE1)
irq = DigitalInOut(board.D22)
rst = DigitalInOut(board.D25)

# retrieve TTN Keys from environment
# TTN device Address, 4 Bytes, MSB
devaddr = getTTNKey("DEVADDR")
# TTN network Key, 16 Bytes, MSB
nwkey = getTTNKey("NWKEY")
# TTN application Key, 16 Bytess, MSB
app = getTTNKey("APP")

# initialize ThingsNetwork configuration
ttn_config = TTN(devaddr, nwkey, app, country=getTTNCountryFromENV())
# initialize lora object
lora = TinyLoRa(spi, cs, irq, rst, ttn_config)

# 2b array to store sensor data
data = bytearray(9)

for meas in range (0, 15, 1):
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('Retrieving data', 10, 0, 1)
    display.show()

    time.sleep(1)
    
    sendDataTTN(getPayloadMockBMP388())
    print("packet sent!")

    time.sleep(2)
