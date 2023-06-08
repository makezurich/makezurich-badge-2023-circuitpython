# Simon says game with touch cover on the MakeZürich 2023 badge
Credit for original code: https://learn.adafruit.com/simon-game-with-pyruler-and-circuitpython/code-pyruler-with-circuitpython

Slightly modified and adapted to our badge

## Required libraries
Import them from the adafruit bundle either manually or automatically with VS code
- neopixel
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
    - Documentation: https://docs.circuitpython.org/projects/neopixel/en/latest/

## Modification needed on the badge-cover
See [README in parent folder](../README.md)

## Play the game
After the initial light wandering sequence (yellow and then blue), one of the 4 corner LEDs wil blink in blue while the status LEDs (the two middle ones) are blue.
Then the status LEDs turn green and it's waiting with a 6 second timeout for a touch.
You now have to touch the corresponding buttons in the right sequence (they light up blue if the touch got registered).
Each round will add a press so the game gets more and more challanging.
