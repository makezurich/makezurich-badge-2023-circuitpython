#
# Requires an analog pin. For example from the analog Grove port on the back.
# Analog pin allow you to convert the analog voltage into a digital value (ADC).

import time
import board
from analogio import AnalogIn

sound = AnalogIn(board.GP27)

while True:
    print("Sound value:", sound.value)
    time.sleep(0.25)
