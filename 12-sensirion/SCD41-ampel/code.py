# MakeZurich Badge 2023
# CO2 Ampel (3 phase status indicator) based on Sensirions SCD41 

# Requires:
#  lib/adafruit_scd4x.mpy
#  lib/adafruit_bus_device - Transient, needed for bus synchronization
#  lib/adafruit_register - Transient, needed for I2C communication
#  lib/neopixel.mpy

import time
import board
import busio
import adafruit_scd4x
import neopixel

# See badge pinout, depending on the connector you use 
# you have to select the corresponding GPIOs used for the I2C communication
# https://github.com/makezurich/makezurich-badge-2023/blob/main/makezurich2023-badge-pinout.png
# The format is busio.I2C(SCL, SDA)
# The example below assumes you used I2C1 on the badge
i2c = busio.I2C(board.GP3, board.GP2)
scd4x = adafruit_scd4x.SCD4X(i2c)

# Setup the LED configuration for the 6 pixels on the badge
pixel_pin = board.GP22
num_pixels = 6

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

# Color definitions
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

# Reset all pixels to black to ensure they are not in an old state while we wait for the first data
pixels.fill(BLACK)
pixels.show()

while True:
    if scd4x.data_ready:
        # For this example, I'm using the values that are also used in the Sensirion SCD41 CO2-Gadget
        # If below 1000ppm, show green
        if scd4x.CO2 < 1000:
            # fill will set all 6 pixels with the same color
            pixels.fill(GREEN)
            print("GREEN")
        # If between 1000ppm and 1600ppm, show yellow
        elif 1000 <= scd4x.CO2 < 1600:
            pixels.fill(YELLOW)
            print("YELLOW")
        # We could have another if or just use the else as this will be reached if no condition matched so far
        # In our case it means it is more than 1600ppm
        else:
            print("RED")
            pixels.fill(RED)
        # After we set all the pixels, let's display the color
        pixels.show()

        # In addition, we still write out the actual measurements to the serial console
        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()
    time.sleep(1)