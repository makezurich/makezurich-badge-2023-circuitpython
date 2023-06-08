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
import os
from rainbowio import colorwheel
import adafruit_simplemath


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
ADC_0 = board.GP26
ADC_1 = board.GP27

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)

INFO_COLORS = {
    'hw': YELLOW,
    'sw': RED,
    'design': BLUE,
    'usecase': GREEN,
}

def scale_tuple(t,factor) -> tuple:
    return tuple([i * factor for i in t])

def fade_tuples(t1,t2,val=0.5) -> tuple:
    val2 = 1 - val
    t1 = scale_tuple(t1,val)
    t2 = scale_tuple(t2,val2)
    return tuple(map(lambda x, y: x + y, t1, t2))

class LEDs:

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

    def set_pixel(self,x,y,color):
        if x > 1:
            x = 1
        if y > 2:
            y = 2
        map = [[1,0,5],[2,3,4]]
        self.pixels[map[x][y]] = color
        self.pixels.show()

    def clear(self):
        self.pixels.fill(BLACK)
        self.pixels.show()

    def fill(self,color):
        self.pixels.fill(color)
        self.pixels.show()

    def show_info(self) -> None:
        self.set_pixel(0,0,(INFO_COLORS[os.getenv("role_1").lower()]))
        self.set_pixel(0,1,(INFO_COLORS[os.getenv("role_2").lower()]))
        self.set_pixel(0,2,(INFO_COLORS[os.getenv("role_3").lower()]))
        if 'true' in os.getenv("photo_allowed").lower():
            self.set_pixel(1,0,GREEN)
        else:
            self.set_pixel(1,0,RED)

    def traffic_light(self,val,threshold_1=33,threshold_2=66) -> None:
        if val < threshold_1:
            self.fill_pixel(GREEN)
        elif val >= threshold_2:
            self.fill_pixel(RED)
        else:
            self.fill_pixel(YELLOW)
    
    def traffic_light_pixel(self,x,y,val,threshold_1=33,threshold_2=66) -> None:
        if val < threshold_1:
            self.set_pixel(x,y,GREEN)
        elif val >= threshold_2:
            self.set_pixel(x,y,RED)
        else:
            self.set_pixel(x,y,YELLOW)

    def gauge(self,val,min=0,max=100,color=BLUE) -> None:
        pixl = adafruit_simplemath.map_range(val, min, max, 0.0, 5.9)
        int_pixl = int(pixl)
        for i in range(0,int_pixl):
            self.pixels[i] = color
        self.pixels[int_pixl] = scale_tuple(color,pixl%1)
        self.pixels.show()

    def fade_pixel(self,x,y,val,color1=GREEN,color2=RED) -> None:
        self.set_pixel(x,y,fade_tuples(color1,color2,val))
        

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