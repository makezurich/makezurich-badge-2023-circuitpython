# Getting Started

## Hardware

* Raspberry Pi Pico W (W stands for Wi-Fi)
* Seed Studio LoRa E5, Pin GP4 + GP5
* 6 Neopixels on Pin GP22
* 1 LED on Pin GP8
* 1 Button on Pin GP6
* 4 expansion ports (Grove)
* 1 PicoW onboard LED, Pin LED

## Installing CircuitPython

**Mind**: CircuitPython should already be installed on your badge.
Therefore, this step is not needed.

1. Download the uf2 file from https://circuitpython.org/board/raspberry_pi_pico_w/
2. While holding the white "BOOTSEL" button connect the pico W to your computer, it should mount as "RPI-RP2"
3. Copy the circuitpython uf2 file onto it
4. After it is done the pico W will mount as "CIRCUITPY"

## Getting libraries

Lots of existing libraries are bundled in the zip, which you can copy paste to your PicoW lib folder.

1. Download v8 from https://circuitpython.org/libraries

> To prevent mistakes I recommend to delete the folders lib/adafruit_featherwing and lib/adafruit_seesaw

## CircuitPython Essentials
Adafruit has a great list of examples on [CircuitPython Essentials](https://learn.adafruit.com/circuitpython-essentials/circuitpython-essentials). Many examples of this repository are taken from there.

## IDE's and extensions that can make your life easier

### VS code

VS code is an easy to use IDE that has a lot of extensions, including extensions for python and also circuit python that safes you some hasle with e.g. adding a specific library to your project (the extensions downloads the latest bundle and places the module you add directly in your lib folder).

See https://code.visualstudio.com for more information and download of Visual Studio Code.

#### Circuit python extension

Get it from the marketplace directly inside VS code, more info can be found in the extension readme:
- Name: CircuitPython
- Id: joedevivo.vscode-circuitpython
- Description: CircuitPython for Visual Studio Code
- Version: 0.1.20
- Publisher: joedevivo
- VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=joedevivo.vscode-circuitpython

## LoRa
Two ways of sending packages:
* Confirmed delivery, you want to know if sending succeeded, send packages with confirmation (ACK).
* Fire and forget, you hope some gateway will receive it. Send without confirmation (no ACK).

> The inital join is only done once to get the session keys, device will store them and stay joined.

### Setting up LoRa OTAA

1. visit the things network EU console https://eu1.cloud.thethings.network/console/
2. you may need to create an account first
3. Create a new application with the name "makezurch-badge-2023-YOURNAME"
4. On your pico run `AT+ID` to get the AppEui (also referenced as JoinEUI), DevEui, DevAddr
5. Register end device
    * manual
    * frequency plan: Europe 863-870 MHz (SF9 for RX2 - recommended)
    * LoRaWAN version: LoRaWAN Specification 1.0.3
    * under "Provisioning Information" for JoinEUI fill in the AppEui
    * also fill the DevEUI as obtained from the AT command
    * Click "Generate" to obtain an AppKey
6. Configure LoRa with the value from Activation Information > AppKey
   1. AT+KEY=APPKEY,"AppKey"

### Sending Packages

We use the UART port on pin GP4 and GP5 to send AT commands to the "Seed Studio LoRa E5".
It uses LoRa Version 1.0.3.

> If you want to play with the AT commands yourself see example 05-lora/serial-debug.py

To set it up

```bash
AT+ID
# -> Use this info to configure your device in the thingsnetwork console
AT+DR=5 # 5 sets the datarate to SF7, which is recommended by thingsnetwork
AT+CH=NUM,0-2 # NOTE(yw): no idea what channel to choose
AT+MODE=LWOTAA # LWOTAA or LWABP, LWOTAA is recommended
AT+KEY=APPKEY,"YOUR_APP_KEY_HERE" # appkey when using LWOTAA
AT+CLASS=A
AT+PORT=8
AT+JOIN
AT+CMSG="Hello"
```

> NOTE: you only need to set the APPKEY once and it is remembered.

You should see in the "Live data" section of your application on
[TheThingsNetwork console](https://eu1.cloud.thethings.network/console/)
an entry of type "Forward uplink data message" with a Payload
"48656C6C6F". You can convert this payload from hexadecimal to ASCII
using e.g. [this webpage](https://www.rapidtables.com/convert/number/hex-to-ascii.html)
and should see that it translates to the "Hello" message sent.

ABP vs OTAA https://www.thethingsindustries.com/docs/devices/abp-vs-otaa/#otaa
[Seed Studio LoRa E5 Documentation](https://files.seeedstudio.com/products/317990687/res/LoRa-E5%20AT%20Command%20Specification_V1.0%20.pdf)

## Knowledge

### Connecting to Serial

On macOS:

```bash
screen /dev/tty.usbmodemXXX 115200
```

### CircuitPython vs Micropython
CircuitPython is a fork of MicroPython that includes a more extensive set of libraries and drivers out of the box, making it easier to get started with. It also has a higher level of abstraction, which can make it easier to write code quickly, and supports a growing number of boards and peripherals.

CircuitPython is heavly maintained by Adafruit, which provides many examples and libraries for all their libraries.

If you see any `import machine` the code is probably using micropython.

## Hardware

### Grove Kit
Examples for the Grove Basic Kit can be found under 06-grove-starterkit.
For more see their [wiki](https://wiki.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico/) with examples in **micropython**.

‼️ Help my kit is incomplete! ‼️ Check with the staff or see if you can swap it with other sensors for example provided by Sensirion

### Sensirion Sensors
[Sensirion](https://www.sensirion.com) sponsored sensors. Examples can be found under `12-sensirion`

* Grove SEN5X All in One [wiki](https://wiki.seeedstudio.com/Grove_SEN5X_All_in_One/)
* Grove - CO2 & Temperature & Humidity Sensor (SCD30) [wiki](https://wiki.seeedstudio.com/Grove-CO2_Temperature_Humidity_Sensor-SCD30/)
* Grove - CO2 & Temperature & Humidity Sensor（SCD41) [wiki](https://wiki.seeedstudio.com/Grove-CO2_&_Temperature_&_Humidity_Sensor-SCD41/)
* Grove Temp&Humi Sensor (SHT40) [wiki](https://wiki.seeedstudio.com/Grove-SHT4x/)

### AP9 box

The MakeZurich Badge fits into a standard AP9 box (80x80x35mm).

![AP9.png](pictures/AP9.png)

## Pinouts

* [MakeZurich Badge](pinout.png)
* [Pico W](picow-pinout.png)

## Questions
* How do you receive packages? You need to send a package and in the response downlink data is included.
* Are the lora configuration values channel, mode, class, appkey persisted? -> Yes
* Can you read out the AT+KEY of a device? -> No, all KEYs are unreadable for security, the one who forgets his KEY need rewrite with a new key.
* How to measure RSSI, is there a command? -> In the TTN console event details, you can inspect what the receiving gateways report (sometimes multiple gateways receive your packets).
* What is a good RSSI? -> Higher than -120 (minimum you can have) and usually below -40 (right next to the gateway).
* Why is OTAA better than ABP? [link](https://www.thethingsindustries.com/docs/devices/abp-vs-otaa/#otaa)
* What does the python package "supervisor" do? It is used to receive data over serial, while being plugged into USB.
* Does every badge have an unique EUI? -> yes
* How much is the difference for LoRa between a handcrafted binary payload vs serialising to JSON text payload?
* What are AT commands? -> AT commands are used in modems and other hardware for querying or setting parameters [more](https://www.commfront.com/pages/at-commands)
* Does CircuitPython support hardware interrupts? -> No, [FAQ](https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio?view=all#faq-3106700)
