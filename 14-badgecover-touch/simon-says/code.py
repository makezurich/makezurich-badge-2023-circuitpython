# MakeZurich Badge 2023
# Simon says game with touch cover
# Credit for original code: https://learn.adafruit.com/simon-game-with-pyruler-and-circuitpython/code-pyruler-with-circuitpython
# Slightly modified and adapted to our badge

# Requires:
#  lib/neopixel.mpy

import time
import board
import touchio
import neopixel
import random
from rainbowio import colorwheel

touches = []
for p in (board.GP9, board.GP19, board.GP28, board.GP14):
    touches.append(touchio.TouchIn(p))

# Setup the LED configuration for the 6 pixels on the badge
pixel_pin = board.GP22
num_pixels = 6

# Setting auto_write to true means that setting a pixel will directly change it without waiting for a show() command
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.4, auto_write=True)

leds = [1, 2, 5, 4]
statusled = [0, 3]

cap_touches = [False, False, False, False]

# Color definitions
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Game configuration
INPUT_TIMEOUT = 6

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(len(statusled)):
            rc_index = (i * 256 // len(statusled)) + j
            pixels[statusled[i]] = wheel(rc_index & 255)
        time.sleep(wait)

def read_caps():
    cap_touches[0] = touches[1].value
    cap_touches[1] = touches[1].value
    cap_touches[2] = touches[2].value
    cap_touches[3] = touches[3].value
    return cap_touches

def timeout_touch(timeout=INPUT_TIMEOUT):
    start_time = time.monotonic() # start a timer waiting for user input
    while time.monotonic() - start_time < timeout:
        caps = read_caps()
        for i,c in enumerate(caps):
            if c:
                return i

def light_cap(cap, duration=0.5):
    # turn the LED for the selected cap on
    pixels[leds[cap]] = BLUE
    time.sleep(duration)
    pixels[leds[cap]] = BLACK
    time.sleep(duration)

def play_sequence(seq):
    duration = max(0.1, 1 - len(sequence) * 0.05)
    for cap in seq:
        light_cap(cap, duration)

def read_sequence(seq):
    setStatusColor(GREEN)
    for cap in seq:
        if timeout_touch() != cap:
            # the player made a mistake!
            return False
        light_cap(cap, 0.5)
    return True

def clearScreen():
    # Reset all pixels to black to ensure they are not in an old state
    pixels.fill(BLACK)

def setStatusColor(color):
    for position in statusled:
        pixels[position] = color

def startAnimation():
    for led in leds:
        pixels[led] = YELLOW
        time.sleep(0.25)
    for led in leds:
        pixels[led] = BLACK
    for led in leds:
        pixels[led] = BLUE
        time.sleep(0.25)
    for led in leds:
        pixels[led] = BLACK

clearScreen()
while True:
    # led light sequence at beginning of each game
    setStatusColor(BLUE)
    print("Play a game of Simon Says")
    time.sleep(1)
    startAnimation()
    sequence = []
    while True:
        setStatusColor(BLUE) # blue for showing user sequence
        time.sleep(1)
        sequence.append(random.randint(0, 3)) # add new light to sequence each time
        play_sequence(sequence) # show the sequence
        if not read_sequence(sequence): # if user inputs wrong sequence, gameover
            # game over, make status red
            setStatusColor(RED)
            time.sleep(3)
            print("gameover")
            break
        else:
            print("Next sequence unlocked!")
            rainbow_cycle(0) # Animation after each correct sequence
        setStatusColor(BLACK) # reset screen
        time.sleep(1)