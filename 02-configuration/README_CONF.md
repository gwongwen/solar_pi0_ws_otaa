
# Configuration

## Step 1 : Installation of requirements and dependencies

The script install can be found in the **02-configuration folder**. This script will enable the I2C and SPI interface, install the BMP388 requirements, the LoRa Radio Bonnet requirements and the Solar Pi Platter drivers (talkpp and ppd). When the script will be done, we recommend you to test both the LoRa module and the BMP388 sensor to verify that everything is working correctly.
All tests can be found in the **01-hardware folder**. We invite you to read the **README_HARD.md** file present in this folder which describes hardware and software of this project.

To run as sudo user, tape : **sudo \\.pp_config_install.sh** or **sudo bash pp_config_install.sh**.

## Step 2 : Configuration of the TTN (The Things Network)

To begin, we will need to login into the ttn (https://www.thethingsnetwork.org/) console. Once this is done (as our sensor is both a gateway and a sender) we need to create both a gateway and an application.

### Application (sender)

You will need to register a new device in your application (with OTAA activation method). Once this is done, retain the End device ID (8 Bytes), the Apllication ID (8 Bytes) and the TTN Application Key (16 Bytes). You also have to make sure that the activation method is OTAA.

    - After you account was created, you have to create a new application : Name of this application --> solar-pi0-ws-app

    - After that, you have to add a new end device on this application. You have to complete the various fields in manually mode :
        Frequency Plan                  Europe 863-870 MHz (SF9 for RX2 - Recommanded)
        LoRaWAN Version                 MAC V1.0.2
        Regional Parameter Version      PHY V1.0.2 REB B
        Activation by personalization   OTAA
        Application ID                  solar-pi0-ws-app
        DevUI                           004764B1ABC64F7C
        AppEUI                          70B3D57ED00485A9
        AppKey                          4AD7B63F86ABC754CF268EE560DE1C99

After the test **test_send_lora_otaa.py** purposed in **01-hardware/tests**, you have to paste the file payload_format into the TTN application decoder function so you can read the packets content in real time already decripted.

# Usage

Once these configuration and installation steps are completed successfully, we will be able to use the connected node autonomously. To do this, we invite you to go to **03-run** folder and read the **READ_RUN.md** document.

# Description of used pins

In this project, we will use :

    - Solar Pi Platter board for Pi Zero V1.3 by danjuliodesigns
    - Raspberry Pi Zero W v1.1
    - Senseor Bosh BMP388 mounted onto BMP3xy extended shuttle board
    - Adafruit Lora Radio Bonnet with Oled - RFM95W @ 915MHz

## Solar Pi Platter board

Connectivity between the Solar Pi Platter board and the raspberry pi zero w is achieved by a simple ASCII character command set sent/received through a CDC-class serial port.

## Adafruit LoRa Radio Bonnet

The LoRa Radio Bonnet will be directly plugged into the board (as it is an all-ensembled board) and will make use of :

**(for the radio module)**

    - RST : Radio reset pin, connected to GPIO25 on the Pi
    - CS : Radio SPI Chip Select pin, connected to SPI CE1 on the Pi
    - CLK : Radio SPI Clock pin, connected to SPI SCLK on the Pi
    - DI : Radio SPI data in pin, connected to SPI MOSI on the Pi
    - DO : Radio SPI data out pin, connected to SPI MISO on the Pi
    - DIO0 : Radio digital IO #0 pin, we use this for status or IRQs It's required for all our examples. Connected to GPIO 22 on the Pi
    - DIO1 : Radio digital IO #1 pin, we use this for status. This is not used for our basic CircuitPython code, but is used by some more advanced libraries. You can cut this trace if you want to use the Pi pin for other devices. Connected to GPIO 23 on the Pi
    - DIO2 : Radio digital IO #2 pin, we use this for status. This is not used for our basic CircuitPython code, but is used by some more advanced libraries. You can cut this trace if you want to use the Pi pin for other devices. Connected to GPIO 24 on the Pi
    - DIO3 : Radio digital IO #3, not connected or used at this time
    - DIO4 : Radio digital IO #3, not connected or used at this time

**(for the oled)**

    - SCL is connected to SCL on the Pi
    - SDA is connected to SDA on the Pi

**(for the buttons)**

    - Button 1 : Connected to GPIO 5 on the Pi
    - Button 2 : Connected to GPIO 6 on the Pi
    - Button 3 : Connected to GPIO 12 on the Pi

#### LoRa Radio Bonnet breakout pinout

    RFM95W      GPIO       
    RST         25
    CS          7 (SPI CE1)
    CLK         11 (SPI SCLK)
    DI          10 (SPI MOSI)
    DO          9 (SPI MISO)
    DIO0        22
    DIO1        23
    DIO2        24
    DIO3        NC
    DIO4        NC
    SCL         3 (SCL)
    SDA         2 (SDA)
    Button1     5
    Button2     6
    Button3     12

## BMP3xy breakout pinout

**todo** Add comments when the daugther PCB for sensor will be made. The idea is to plug a board above the Adafruit LoRa bonnet with tne same pinout (GPIO of standard Pi Zero).


# Documentation about talkpp/ppd drivers

This directory contains Raspbian utility software for the Solar Pi Platter board.

## talkpp

talkpp is a utility program to simplify communicating with the Solar Pi Platter board. It provides a simple command-line interface to allow the user to directly (or via scripts) send commands to the board and to easily manage the Real Time Clock.  

It can communicate with the board via either the pseudo-tty /dev/pi-platter if the ppd daemon is running or the actual hardware serial device associated with the board if ppd is not running.  It uses udev to automatically find the correct serial device for the board, independent of other USB serial devices.

### Dependencies install

Install of libudev - API for enumerating and introspecting local devices :

    sudo apt-get update
    sudo apt-get install libudev-dev

### Manual install

Both the source and a binary compiled under Raspbian Jessie are included.  The binary can simply be downloaded and installed in /usr/local/bin.  The source is easily compiled in the directory containing the source file.

    gcc -o talkpp talkpp.c -ludev
    sudo cp talkpp /usr/local/bin
    sudo chmod 775 /usr/local/bin/talkpp

### Usage

talkpp takes the following arguments :

    talkpp [-c <command string>]

          [-s] [-t] [-f]

          [-a <alarm timespec>] [-d <delta seconds>] [-w]

          [-u | -h]


    -c <command string> : send the command string.  Command strings without an "=" character cause the utility to echo back a response.

    -s : Set the Device RTC with the current system clock
 
    -t : Get the time from the Device RTC and display it in a form useful to pass to "date" to set the system clock ("+%m%d%H%M%Y.%S")

    -f : Get the time from the Device RTC and display it in a readable form.

    -a <alarm timespec> : Set the Device wakeup value (does not enable the alarm).  <alarm timespec> is the alarm time in date time format ("+%m%d%H%M%Y.%S")

    -d <delta seconds> : Set the Device wakeup to <delta seconds> past the current Device RTC time value (does not enable the alarm)

    -w : Display the wakeup value in a readable form.

    -u, -h : Usage (and optional help)


Example command to Solar Pi Platter: `talkpp -c B`

Setting the Solar Pi Platter RTC from the Pi's RTC: `talkpp -s`

Setting the Pi's RTC from the Solar Pi Platter (using BASH): `sudo date $(talkpp -t)`

talkpp will echo responses from the Solar Pi Platter to stdout.  It will also echo the last warnings or error messages that has been sent.

## ppd

ppd is a daemon for the Solar Pi Platter.  It provides two main functions.  It will execute a controlled shutdown if the Solar Pi_Platter detects a critical battery voltage (and will power-down the entire system after [default] 30 seconds).  Since it opens the serial port associated with the Solar Pi Platter it also provides one or two mechanisms for other applications to communicate with the Solar Pi Platter.  It creates a pseudo-tty device named /dev/pi-platter which can be used just like the hardware serial port.  It also, optionally, can create a TCP port for applications like telnet to connect to.  

It is important that software not open the hardware serial port, /dev/ttyACM<n>, when ppd is running since it is using the port.

### Manual install

Both the source and a binary compiled under Raspbian Jessie are included. The binary can simply be downloaded and installed in /usr/local/bin. The source is easily compiled in the directory containing the source file.

    gcc -o ppd ppd.c -ludev
    sudo cp ppd /usr/local/bin
    sudo chmod 775 /usr/local/bin/ppd

### Usage

There are many ways to start a daemon, for example a configuration file in / or a script in /etc/init.d.  A very easy way to start it is to include it in /etc/rc.local.  For example, add the following before the "exit 0" at the end of /etc/rc.local (assuming you have placed the ppd executable in /usr/local/bin).

    /usr/local/bin/ppd -p 23000 -r -d &

It is also possible to create a conf file in /etc/init or a startup script in /etc/init.d.

ppd takes the following command line arguments:

    -d : Run as a daemon program (disconnecting from normal IO, etc).  ppd can be run as a traditional process without this argument.

    -p netport : Enable a TCP socket connection on the specified port.  This is required to enable socket communication with ppd.  Exclude this line to only enable /dev/pi-platter as a mechanism to communicate with the Solar Pi Platter.

    -m max-connections : Specify the maximum number of socket connections that can be made to the port specified with -p.  The default is 1.

    -r : Enable auto-restart on charge (set the Pi Platter "C7=1") after critical battery shutdown.

    -x debuglevel : Set the debug level (ppd uses the system logging facility.  0 is default (only log start-up).  Values of 1 - 3 include progressively more information.

    -h : Display usage and command line options.

This starts ppd with socket communication available on port 23000 and auto-restart in the event of a critical battery shutdown.



