# MakeZurich Badge 2023
# SCD30 Simple Example

# Requires:
#  lib/adafruit_scd30.mpy
#  lib/adafruit_bus_device - Transient, needed for bus synchronization
#  lib/adafruit_register - Transient, needed for I2C communication

import time
import board
import busio
import adafruit_scd30

# See badge pinout, depending on the connector you use 
# you have to select the corresponding GPIOs used for the I2C communication
# https://github.com/makezurich/makezurich-badge-2023/blob/main/makezurich2023-badge-pinout.png
# The format is busio.I2C(SCL, SDA)
# The example below assumes you used I2C1 on the badge

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
i2c = busio.I2C(board.GP3, board.GP2, frequency=50000)
scd30 = adafruit_scd30.SCD30(i2c)

while True:
    # since the measurement interval is long (2+ seconds) we check for new data before reading
    # the values, to ensure current readings.
    if scd30.data_available:
        print("Data Available!")
        print("CO2:", scd30.CO2, "PPM")
        print("Temperature:", scd30.temperature, "degrees C")
        print("Humidity:", scd30.relative_humidity, "%%rH")
        print()
        print("Waiting for new data...")
        print()

    time.sleep(0.5)
