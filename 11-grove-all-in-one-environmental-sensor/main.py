import time

import board
import busio

from sensirion_i2c_driver import I2cTransceiver, I2cConnection
from sensirion_i2c_sen5x import Sen5xI2cDevice

# The address can be found on the back of the Grove All-in-one Environmental Sensor
SEN5X_DEFAULT_ADDRESS = 0x69

# setup i2c - see CircuitPython docs, or get from board
# https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/pinouts#no-default-board-devices-3082902
i2c = busio.I2C(scl=board.GP3, sda=board.GP2)
transceiver = I2cTransceiver(i2c, SEN5X_DEFAULT_ADDRESS)
device = Sen5xI2cDevice(I2cConnection(transceiver))

# Perform a device reset (reboot firmware)
device.device_reset()

# Print some device information
print("Product Name: {}".format(device.get_product_name()))
print("Serial Number: {}".format(device.get_serial_number()))
print("Version: {}\n".format(device.get_version()))

# Start measurement
device.start_measurement()
for i in range(20):
    # Wait until next result is available
    print("Waiting for new data...")
    while not device.read_data_ready():
        time.sleep(1.0)

    # Read measured values -> clears the "data ready" flag
    values = device.read_measured_values()
    print(values)

    # Access a specific value separately (see Sen5xMeasuredValues)
    mass_concentration = values.mass_concentration_2p5.physical
    ambient_temperature = values.ambient_temperature.degrees_celsius

    # Read device status
    status = device.read_device_status()
    print("Device Status: {}\n".format(status))
    time.sleep(5.0)

# Stop measurement
device.stop_measurement()
print("Measurement stopped.")