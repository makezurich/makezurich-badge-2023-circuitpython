# The RGB LED hardware is WS2813, which can be controlled by neopixel library.
# from https://learn.adafruit.com/circuitpython-essentials/circuitpython-neopixel

# Requires:
#  lib/neopixel.mpy

import time
import board
import neopixel

pixel_pin = board.GP3
num_pixels = 1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

while True:
    pixels.fill(RED)
    pixels.show()
    time.sleep(1)
    pixels.fill(GREEN)
    pixels.show()
    time.sleep(1)
    pixels.fill(BLUE)
    pixels.show()
    time.sleep(1)
