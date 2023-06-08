# MakeZurich Badge 2023
# Simple example on using the touch buttons from the cover

# Requires:
#  lib/neopixel.mpy

import time
import board
import touchio
import neopixel

# GP9, GP19, GP28 and GP14 connect to the touchpad (or a simple wire) and from there it needs 
# a 1M Ohm resistor to GND
# see readme for needed extension to be made to the cover in order for this to work
tp1 = touchio.TouchIn(board.GP9)
tp2 = touchio.TouchIn(board.GP19)
tp3 = touchio.TouchIn(board.GP28)
tp4 = touchio.TouchIn(board.GP14)

# Setup the LED configuration for the 6 pixels on the badge
pixel_pin = board.GP22
num_pixels = 6

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.4, auto_write=False)

# Color definitions
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Reset all pixels to black to ensure they are not in an old state while we wait for the first data
pixels.fill(BLACK)
pixels.show()

while True:
    print("TP1 = ", tp1.value)
    if(tp1.value):
        pixels[1] = RED
    else:
        pixels[1] = BLACK
    print("TP2 = ", tp2.value)
    if(tp2.value):
        pixels[2] = GREEN
    else:
        pixels[2] = BLACK
    print("TP3 = ", tp3.value)
    if(tp3.value):
        pixels[5] = YELLOW
    else:
        pixels[5] = BLACK
    print("TP4 = ", tp4.value)
    if(tp4.value):
        pixels[4] = BLUE
    else:
        pixels[4] = BLACK
    pixels.show()
    time.sleep(0.1)
