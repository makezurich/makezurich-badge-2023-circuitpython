# same code as controlling a simple LED

import time
import board
import digitalio

btn = digitalio.DigitalInOut(board.GP6)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

relay = digitalio.DigitalInOut(board.GP3)
relay.direction = digitalio.Direction.OUTPUT

btn_previous_state = True

while True:
    btn_current_state = btn.value
    # Only handling button key press down (if button is pressed then voltage on the pin is low, which equals to False)
    if btn_current_state != btn_previous_state and btn_current_state == False:
        print("Button was pressed")
        print("Setting relay to", not relay.value)
        relay.value = not relay.value

    btn_previous_state = btn_current_state
