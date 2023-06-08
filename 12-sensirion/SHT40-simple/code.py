# MakeZurich Badge 2023
# SHT40 Simple Example

# Requires:
#  lib/adafruit_scd4x.mpy
#  lib/adafruit_bus_device - Transient, needed for bus synchronization
#  lib/adafruit_register - Transient, needed for I2C communication

import time
import board
import busio
import adafruit_sht4x

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

while True:
    temperature, relative_humidity = sht40.measurements
    print("Temperature: %0.1f C" % temperature)
    print("Humidity: %0.1f %%" % relative_humidity)
    print("")
    time.sleep(1)