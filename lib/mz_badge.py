# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 morgulbrut
#
# SPDX-License-Identifier: MIT
"""
`mz_badge`
================================================================================

Utilities for the MZ2023 badge


* Author(s): Tillo

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

import time
import board
import busio
import neopixel
from rainbowio import colorwheel


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/morgulbrut/CircuitPython_mz_badge.git"

UART_LORA = busio.UART(board.GP4, board.GP5, baudrate=9600)
NEO_PXL = board.GP22
LED = board.GP8
BUTTON = board.GP6
TX_0 = board.GP0
RX_0 = board.GP1
SDA_0 = board.GP20
SCL_0 = board.GP21
SDA_1 = board.GP2
SCL_1 = board.GP3

class Neopixel:
    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    BLACK = (0, 0, 0)

    def __init__(self,pin=NEO_PXL):
        self.pin = pin
        self.num_pixels = 6
        self.pixels = neopixel.NeoPixel(self.pin, self.num_pixels, brightness=0.3, auto_write=False)

    def color_chase(self,color, wait):
        for i in range(self.num_pixels):
            self.pixels[i] = color
            time.sleep(wait)
            self.pixels.show()
        time.sleep(0.5)

    def rainbow_cycle(self,wait):
        for j in range(255):
            for i in range(self.num_pixels):
                rc_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = colorwheel(rc_index & 255)
            self.pixels.show()
            time.sleep(wait)

class LoRa_module:

    def __init__(self,uart=UART_LORA) -> None:
        self.uart = uart

    def show_information(self)-> None:
        self.at_send('AT+CH')
        self.at_send('AT+MODE')
        self.at_send('AT+ID')

    def set_mode(self,mode)-> None:
        self.at_send(f'AT+MODE={mode}')

    def setup_and_join_otaa(self,appkey, appeui) -> bool:
        self.set_mode('OTAA')
        self.at_send(f'AT+KEY=APPKEY, {appkey}')
        self.at_send(f'AT+ID=APPEUI, {appeui}')
        return self.join()

    def join(self) -> bool:
        self.at_send('AT+JOIN')
        data = self.uart.readline() 
        while data is  None:
            time.sleep(.2)
            data = self.uart.readline()
        data_string = ''.join([chr(b) for b in data])
        print(f'<-- {data_string}', end="")
        if "failed" in data_string:
            return False
        else:
            return True

    def send(self, mode,data)-> None:
        self.at_send(f'AT+{mode}={data}')
        while data is  None:
            time.sleep(.2)
            data = self.uart.readline()
        print(f'Sent: {data}')


    def send_hex(self,data)-> None:
        self.at_send(f'AT+MSGHEX={data}')
        while data is  None:
            time.sleep(.2)
            data = self.uart.readline()
        print(f'Sent: {data}')

    def send_string(self,data)-> None:
        self.at_send(f'AT+MSG={data}')
        while data is  None:
            time.sleep(.2)
            data = self.uart.readline()
        print(f'Sent: {data}')

    def send_confirmed_hex(self,data)-> None:
        self.at_send(f'AT+CMSGHEX={data}')
        while data is  None:
            time.sleep(.2)
            data = self.uart.readline()
        print(f'Sent: {data}')

    def send_confirmed_string(self,data)-> None:
        self.at_send(f'AT+CMSG={data}')
        while data is  None:
            time.sleep(.2)
            data = self.uart.readline()
        print(f'Sent: {data}')

    def at_send(self,cmd)-> None:
        print(f'--> {cmd}')
        self.uart.write(bytes(cmd,'utf-8'))
        data = self.uart.readline() 
        while data is not None:
            # convert bytearray to string
            data_string = ''.join([chr(b) for b in data])
            print(f'<-- {data_string}', end="")
            data = self.uart.readline()