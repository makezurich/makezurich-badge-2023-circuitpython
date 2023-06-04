# from https://learn.adafruit.com/multi-tasking-with-circuitpython/buttons

import time
import board
import digitalio

btn = digitalio.DigitalInOut(board.GP3)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

previous_state = btn.value

while True:
    current_state = btn.value
    if current_state != previous_state:
        if not current_state:
            print("BTN is down")
        else:
            print("BTN is up")

    previous_state = current_state
