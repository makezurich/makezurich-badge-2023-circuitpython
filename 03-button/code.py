# from https://learn.adafruit.com/multi-tasking-with-circuitpython/buttons

import time
import board
import digitalio

btn = digitalio.DigitalInOut(board.GP6)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.GP8)
led.direction = digitalio.Direction.OUTPUT

btn_previous_state = True

while True:
    btn_current_state = btn.value
    # Only handling button key press down (if button is pressed then voltage on the pin is low, which equals to False)
    if btn_current_state != btn_previous_state and btn_current_state == False:
        print("Button was pressed")
        print("Setting led to", not led.value)
        led.value = not led.value

    btn_previous_state = btn_current_state
