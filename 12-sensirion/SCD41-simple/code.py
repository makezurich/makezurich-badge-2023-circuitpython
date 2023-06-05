# MakeZurich Badge 2023
# SCD41 Simple Example

# Requires:
#  lib/adafruit_scd4x.mpy
#  lib/adafruit_bus_device - Transient, needed for bus synchronization
#  lib/adafruit_register - Transient, needed for I2C communication

import time
import board
import busio
import adafruit_scd4x

# See badge pinout, depending on the connector you use 
# you have to select the corresponding GPIOs used for the I2C communication
# https://github.com/makezurich/makezurich-badge-2023/blob/main/makezurich2023-badge-pinout.png
# The format is busio.I2C(SCL, SDA)
# The example below assumes you used I2C1 on the badge

i2c = busio.I2C(board.GP3, board.GP2)
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

while True:
    if scd4x.data_ready:
        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()
    time.sleep(1)