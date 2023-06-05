# MakeZurich Badge 2023
# SHT40 Example that displays a color according to the meassured teperature

# Requires:
#  lib/adafruit_scd4x.mpy
#  lib/adafruit_bus_device - Transient, needed for bus synchronization
#  lib/adafruit_register - Transient, needed for I2C communication
#  lib/simpleio - Range mapping helper

import time
import board
import busio
import adafruit_sht4x
import neopixel
import simpleio
from rainbowio import colorwheel

# Mapping values for selecting the colors, adjust if you need different temperatures
# Try playing around with the range and see how it behaves
# minimum expected temperature
min_temp = 0
# maximum expected temperature
max_temp = 40

# Setup the LED configuration for the 6 pixels on the badge
pixel_pin = board.GP22
num_pixels = 6
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

# Color definitions
BLACK = (0, 0, 0)

# See badge pinout, depending on the connector you use 
# you have to select the corresponding GPIOs used for the I2C communication
# https://github.com/makezurich/makezurich-badge-2023/blob/main/makezurich2023-badge-pinout.png
# The format is busio.I2C(SCL, SDA)
# The example below assumes you used I2C1 on the badge
i2c = busio.I2C(board.GP3, board.GP2)
sht40 = adafruit_sht4x.SHT4x(i2c)
print("Found SHT4x with serial number", hex(sht40.serial_number))

sht40.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht40.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
print("Current mode is: ", adafruit_sht4x.Mode.string[sht40.mode])

# Reset all pixels to black to ensure they are not in an old state while we wait for the first data
pixels.fill(BLACK)
pixels.show()

while True:
    temperature, relative_humidity = sht40.measurements
    # Map temp to range
    t_color = simpleio.map_range(temperature, min_temp, max_temp, 255, 0)
    # adjust color based on temperature
    pixels.fill(colorwheel(t_color))
    pixels.show()
    print("Temperature: %0.1f C" % temperature)
    print("Humidity: %0.1f %%" % relative_humidity)
    print("Color RGB: %s" % colorwheel(t_color))
    time.sleep(1)