# from https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/blinky-and-a-button

import time
import board
import digitalio

led = digitalio.DigitalInOut(board.GP8)
led.direction = digitalio.Direction.OUTPUT

onboard_led = digitalio.DigitalInOut(board.LED)
onboard_led.direction = digitalio.Direction.OUTPUT


while True:
    led.value = True
    onboard_led.value = True
    time.sleep(0.5)
    led.value = False
    onboard_led.value = False
    time.sleep(0.5)
