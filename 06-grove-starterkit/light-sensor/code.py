# from https://learn.adafruit.com/sensor-plotting-with-mu-and-circuitpython/light
# Requires an analog pin. For example from the analog Grove port on the back.
# Analog pin allow you to convert the analog voltage into a digital value (ADC).

import time
import board
from analogio import AnalogIn

light = AnalogIn(board.GP27)

while True:
    print("raw:", light.value) # raw measured voltage value

    # our own invented light measure unit (needs improvement)
    light_value_that_makes_sense = round(light.value / 10000)
    print("custom", light_value_that_makes_sense)
    time.sleep(.5) # Wait a bit before checking all again
