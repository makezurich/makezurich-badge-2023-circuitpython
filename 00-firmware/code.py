# MakeZurich Badge 2023

# Requires:
#  lib/neopixel.mpy

import time
import board
from rainbowio import colorwheel
import neopixel
import digitalio

pixel_pin = board.GP22
num_pixels = 6
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

btn = digitalio.DigitalInOut(board.GP6)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)
effects = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, BLACK]

previous_state = btn.value
current_effect = 0

rainbow_cycle(0)

while True:
    current_state = btn.value
    if current_state != previous_state:
        if not current_state:
            print("Button is down")
        else:
            print("Button is up")
            color_chase(effects[current_effect], 0.1)  # Increase the number to slow down the color chase
            current_effect = current_effect + 1
            print(current_effect, len(effects))
            if current_effect >= len(effects):
                current_effect = 0

    previous_state = current_state
