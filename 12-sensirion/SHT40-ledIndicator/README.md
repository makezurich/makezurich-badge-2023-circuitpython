# LED Indicator example on using the Groove SHT40 sensor on the MakeZürich 2023 badge
Temperature and Humidity sensor from Sensirion.
Ask someone from the MakeZürich Team if you need one for your project.

This example will use the Neopixel on the badge and maps the sensor reading in a defined range to a color from the color wheel to visualy indicate the measurement.

## Required libraries
Import them from the adafruit bundle either manually or automatically with VS code
- adafruit_sht4x
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_SHT4x
    - Documentation: https://docs.circuitpython.org/projects/sht4x/en/latest/
- adafruit_bus_device
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
- adafruit_register
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_Register
    - Documentation: https://docs.circuitpython.org/projects/register/en/latest/
- neopixel
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
    - Documentation: https://docs.circuitpython.org/projects/neopixel/en/latest/
- simpleio
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_SimpleIO
    - Documentation: https://docs.circuitpython.org/projects/simpleio/en/latest/api.html

## Connecting it to the badge
The sample code assumes you used I2C1 on the badge, you will need to adjust the GPIOs for SCL and SDA accordingly if you used another connector port.

## Datasheet
- https://sensirion.com/resource/datasheet/sht4x

## More information
- https://learn.adafruit.com/adafruit-sht40-temperature-humidity-sensor/python-circuitpython
- https://sensirion.com/products/catalog/SHT40
- https://learn.adafruit.com/neopixel-sprite-weather-display/code-the-weather-display
