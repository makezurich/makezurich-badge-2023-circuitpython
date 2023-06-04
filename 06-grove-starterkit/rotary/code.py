# from https://learn.adafruit.com/make-it-change-potentiometers/circuitpython
# Requires an analog pin. For example from the analog Grove port on the back

import time
import board
from analogio import AnalogIn

potentiometer = AnalogIn(board.GP27)

while True:
    print(potentiometer.value)
    time.sleep(0.25) # Wait a bit before checking all again
