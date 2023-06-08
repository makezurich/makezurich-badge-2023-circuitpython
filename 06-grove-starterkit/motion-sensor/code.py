# from https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/circuitpython-code
# https://en.wikipedia.org/wiki/Passive_infrared_sensor
# NOTE(yw): during testing this sensor was detecting all the time, we did not hav time to fully investigate

import board
import digitalio

LED_PIN = board.GP8   # Pin number for the board's built in LED.
PIR_PIN = board.GP2   # Pin number connected to PIR sensor output wire.

# Setup digital input for PIR sensor:
pir = digitalio.DigitalInOut(PIR_PIN)
pir.direction = digitalio.Direction.INPUT

# Setup digital output for LED:
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT

# Main loop that will run forever:
old_value = pir.value
while True:
    pir_value = pir.value
    if pir_value:
        # PIR is detecting movement! Turn on LED.
        led.value = True
        # Check if this is the first time movement was
        # detected and print a message!
        if not old_value:
            print('Motion detected!')
    else:
        # PIR is not detecting movement. Turn off LED.
        led.value = False
        # Again check if this is the first time movement
        # stopped and print a message.
        if old_value:
            print('Motion ended!')
    old_value = pir_value
