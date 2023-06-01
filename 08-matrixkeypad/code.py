# from https://learn.adafruit.com/matrix-keypad

# Requires:
#  lib/adafruit_matrixkeypad.mpy

import time
import digitalio
import board
import adafruit_matrixkeypad

# The keypad is a matrix, first half o the pins is rows, second half of the pins is columns
# adjust the example for your hardware
rows = [digitalio.DigitalInOut(x) for x in (board.GP28, board.GP12, board.GP13)]
cols = [digitalio.DigitalInOut(x) for x in (board.GP14, board.GP11, board.GP10)]

# keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))
keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

while True:
    keys = keypad.pressed_keys
    if keys:
        print("Pressed: ", keys)
        if 2 in keys:
            print("pressed 2")
    time.sleep(0.2)
