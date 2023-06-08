# MakeZurich Badge 2023
# PWM example to controll the Grove Mini Fan v1.1 with the badge

# Requires:
#  

import time
import board
import pwmio

# For fine fan control, connect it to the ADC Groove port (We need GP26)
# It's in the back of the badge in the left port (the one just next to the pico USB cable)

fan = pwmio.PWMOut(board.GP26, frequency=5000, duty_cycle=0)

while False:
    for i in range(200):
        # PWM Fan up and down
        if i < 100:
            fan.duty_cycle = int(i * 2 * 65535 / 200)  # Up
        else:
            fan.duty_cycle = 65535 - int((i - 100) * 2 * 65535 / 200)  # Down
        time.sleep(0.5)