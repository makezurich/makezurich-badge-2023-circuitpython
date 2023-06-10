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
try:
    tp1 = touchio.TouchIn(board.GP9)
except ValueError:
    print("TP1 has no pulldown")
try:
    tp2 = touchio.TouchIn(board.GP19)
except ValueError:
    print("TP2 has no pulldown")
try:
    tp3 = touchio.TouchIn(board.GP28)
except ValueError:
    print("TP3 has no pulldown")
try:
    tp4 = touchio.TouchIn(board.GP14)
except ValueError:
    print("TP4 has no pulldown")

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
    try:
        print("TP1 = ", tp1.value)
        if(tp1.value):
            pixels[1] = GREEN
        else:
            pixels[1] = BLUE
    except NameError:
        pixels[1] = RED
    try:
        print("TP2 = ", tp2.value)
        if(tp2.value):
            pixels[2] = GREEN
        else:
            pixels[2] = BLUE
    except NameError:
        pixels[2] = RED
    try:
        print("TP3 = ", tp3.value)
        if(tp3.value):
            pixels[5] = GREEN
        else:
            pixels[5] = BLUE
    except NameError:
        pixels[5] = RED
    try:
        print("TP4 = ", tp4.value)
        if(tp4.value):
            pixels[4] = GREEN
        else:
            pixels[4] = BLUE
    except NameError:
        pixels[4] = RED
    pixels.show()
    time.sleep(0.1)
