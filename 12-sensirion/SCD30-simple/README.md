# Simple example on using the Groove SCD30 sensor on the MakeZürich 2023 badge
CO2, Temperature and Humidity sensor from Sensirion.
Ask someone from the MakeZürich Team if you need one for your project.

## Required libraries
Import them from the adafruit bundle either manually or automatically with VS code
- adafruit_scd30
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_SCD30
    - Documentation: https://docs.circuitpython.org/projects/scd30/en/latest/
- adafruit_bus_device
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
- adafruit_register
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_Register
    - Documentation: https://docs.circuitpython.org/projects/register/en/latest/

## Connecting it to the badge
The sample code assumes you used I2C1 on the badge, you will need to adjust the GPIOs for SCL and SDA accordingly if you used another connector port.

## Datasheet
- https://sensirion.com/resource/datasheet/scd30

## More information
- https://learn.adafruit.com/adafruit-scd-40-and-scd-41/python-circuitpython
- https://sensirion.com/products/catalog/SCD30/
- https://www.pcbway.com/blog/technology/Raspberry_Pi_Pico_i2c_devices_with_CircuitPython.html
