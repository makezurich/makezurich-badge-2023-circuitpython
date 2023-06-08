# CO2 Ampel (3 phase status indicator) based on Sensirions SCD41  on the MakeZürich 2023 badge
SCD41 is a CO2, Temperature and Humidity sensor from Sensirion.
Ask someone from the MakeZürich Team if you need one for your project.

For this example, I'm using the values that are also used in the Sensirion SCD41 CO2-Gadget which are:
- Green:    < 1000ppm
- Yellow:   1000ppm - 1600ppm
- Red:      > 1600ppm

## Required libraries
Import them from the adafruit bundle either manually or automatically with VS code
- adafruit_scd4x
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_SCD4X
    - Documentation: https://docs.circuitpython.org/projects/scd4x/en/latest/
- adafruit_bus_device
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
- adafruit_register
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_Register
    - Documentation: https://docs.circuitpython.org/projects/register/en/latest/
- neopixel
    - Source: https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
    - Documentation: https://docs.circuitpython.org/projects/neopixel/en/latest/

## Connecting it to the badge
The sample code assumes you used I2C1 on the badge, you will need to adjust the GPIOs for SCL and SDA accordingly if you used another connector port.

## Datasheet
- https://www.sensirion.com/media/documents/E0F04247/631EF271/CD_DS_SCD40_SCD41_Datasheet_D1.pdf
