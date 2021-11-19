from dotenv import load_dotenv
import threading,time,subprocess,busio,board,adafruit_ssd1306,os,sys,random
from digitalio import DigitalInOut, Direction, Pull
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
from pathlib import Path
import adafruit_bmp3xx

# Updates the Sleep time on the environment and on the 
# .env.dynamic file
# PARAMS: 
# - env-file: name of the file in which update the time value
# - value: new sleep time value
# ATENTION: this method will crush the env_file and create another one
# containing only that line
#
# RETRUN: None
def setNewSleepTime(env_file, value):
    dynamic_env_file = open(env_file, "w")
    dynamic_env_file.write("export SLEEPTIME = "+str(value))
    dynamic_env_file.close()
    os.environ[key] = value

# Get the TTN key from the env and pass it to bytearray
# PARAMS: 
# - key: key needed (must be on the .env file)
# RETRUN: bytearray key value     
def getTTNKey(key):
    try:
        key_to_retrieve_string = os.getenv(key)
        key_to_retrieve_bytearray = bytearray.fromhex(key_to_retrieve_string)
        return key_to_retrieve_bytearray
    except Exception:
        print("Error retrieving TTN key")
        print(sys.exc_info())
        sys.exit()

# Get the TTN country code as an string
# PARAMS: None
# RETRUN: string country code value 
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

# Generate fake data body
# PARAMS: None
# RETRUN: data encoded
def getPayloadMockBMP388():
    press_val = bmp.pressure
    temp_val = bmp.temperature + temperature_offset
    alt_val = bmp.altitude
    return encodePayload(press_val,temp_val,alt_val)

# Encodes payload
# PARAMS: pressure, temperature, gas, altitude and humidity from BME 680 sensor
# RETRUN: data encoded
def encodePayload(pressure,temperature,altitude):
    # Encode float as int
    press_val = int(pressure * 100) 
    temp_val = int(temperature * 100)
    alt_val = int(altitude * 100)
    abs_temp_val = abs(temp_val)

    # Encode payload as bytes
    # Pressure (needs 3 bytes)
    data[0] = (press_val >> 16) & 0xff
    data[1] = (press_val >> 8) & 0xff
    data[2] = press_val & 0xff

    # Temperature (needs 3 bytes 327.67 max value) (signed int)
    if(temp_val < 0):
        data[3] = 1 & 0xff
    else:
        data[3] = 0 & 0xff
    data[4] = (abs_temp_val >> 8) & 0xff
    data[5] = abs_temp_val & 0xff

    # Altitude (needs 3 bytes)
    data[6] = (alt_val >> 16) & 0xff
    data[7] = (alt_val >> 8) & 0xff
    data[8] = alt_val & 0xff

    return data

# Send data
# PARAMS: data
# RETURN: None
def sendDataTTN(data):
    lora.send_data(data, len(data), lora.frame_counter)
    lora.frame_counter += 1
    display.fill(0)
    display.text('Packet sent', 10, 0, 1)
    display.show()

#init env 
loadEnv('.env')
loadEnv('.env.dynamic')
 
# Create the I2C interface.
i2c = busio.I2C()
 
# Create library object using our Bus I2C port
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bmp.sea_level_pressure = 1013.25

bmp.pressure_oversampling = 1
bmp.temperature_oversampling = 1

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5
 
# TinyLoRa Configuration
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.CE1)
irq = DigitalInOut(board.D22)
rst = DigitalInOut(board.D25)

# Retrieve TTN Keys from environment
# TTN Device Address, 4 Bytes, MSB
devaddr = getTTNKey("DEVADDR")
# TTN Network Key, 16 Bytes, MSB
nwkey = getTTNKey("NWKEY")
# TTN Application Key, 16 Bytess, MSB
app = getTTNKey("APP")

# Initialize ThingsNetwork configuration
ttn_config = TTN(devaddr, nwkey, app, country=getTTNCountryFromENV())

# Initialize lora object
lora = TinyLoRa(spi, cs, irq, rst, ttn_config)

# 2b array to store sensor data
data = bytearray(14)

for meas in range (0, 15, 1):
    packet = None
    sendDataTTN(getPayloadMockBMP388())
    time.sleep(2)

