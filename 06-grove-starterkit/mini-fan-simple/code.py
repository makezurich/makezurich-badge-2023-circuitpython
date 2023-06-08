# MakeZurich Badge 2023
# Simple example to controll the Grove Mini Fan v1.1 with the badge

# Requires:
#  

import time
import board
import digitalio

# For simple On/Off control, connect it to any Groove port (digital output needed)
# In this example, it's in the back of the badge in the left port (the one just next to the pico USB cable)
# GP27 is the yellow cable and goes to A5 on the Fan controller board which has a 1M Ohm pull down and acts as On / Off switch
# Note that the whole PWM logic is embedded on the ATMEGA168 to handle smoth operation
fan = digitalio.DigitalInOut(board.GP27)
fan.direction = digitalio.Direction.OUTPUT

while True:
    fan.value = True
    time.sleep(1)
    fan.value = False
    time.sleep(2)