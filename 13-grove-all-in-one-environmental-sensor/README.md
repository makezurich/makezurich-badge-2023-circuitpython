# Getting started guide for Grove SEN5X All in One

This guide explains how to successfully connect the Grove SEN5X All in One sensor
to the Make Zürich badge.

## Resources

* [https://wiki.seeedstudio.com/Grove_SEN5X_All_in_One](https://wiki.seeedstudio.com/Grove_SEN5X_All_in_One)

## Required Python libraries

### Adafruit

Go to [https://circuitpython.org/libraries](https://circuitpython.org/libraries)
and [download the bundle for version 8.x](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20230604/adafruit-circuitpython-bundle-8.x-mpy-20230604.zip).
Unzip the bundle and copy `adafruit-circuitpython-bundle-8.x-mpy-20230604/lib/adafruit_logging.mpy` to
`CIRCUITPY/lib/adafruit_logging.mpy`.

### Sensirion

The author of this [GitHub issue](https://github.com/Sensirion/python-i2c-sen5x/issues/3)
forked two GitHub repositories from Sensirion and implemented modifications to make
the two required Python libraries compatible with [CircuitPython](https://circuitpython.org/).

As a reference, these are the two forked repositories and the relevant pull requests:

* [https://github.com/good-enough-technology/CircuitPython_sensirion_i2c_driver](https://github.com/good-enough-technology/CircuitPython_sensirion_i2c_driver)
* [https://github.com/good-enough-technology/CircuitPython_sensirion_i2c_sen5x](https://github.com/good-enough-technology/CircuitPython_sensirion_i2c_sen5x)
* [https://github.com/Sensirion/python-i2c-driver/compare/master...good-enough-technology:python-i2c-driver:master](https://github.com/Sensirion/python-i2c-driver/compare/master...good-enough-technology:python-i2c-driver:master)
* [https://github.com/Sensirion/python-i2c-sen5x/compare/master...good-enough-technology:circuitpython-i2c-sen5x:master](https://github.com/Sensirion/python-i2c-sen5x/compare/master...good-enough-technology:circuitpython-i2c-sen5x:master)

To obtain the required copy, clone the two repositories:

```shell
git clone --branch master --single-branch --depth 1 https://github.com/good-enough-technology/CircuitPython_sensirion_i2c_driver.git
git clone --branch master --single-branch --depth 1 https://github.com/good-enough-technology/CircuitPython_sensirion_i2c_sen5x.git
```

Modify `CircuitPython_sensirion_i2c_sen5x/sensirion_i2c_sen5x/commands/generated.py`
on line 1129:

```python
- firmware_debug = bool(unpack(">?", checked_data[2:3])[0])  # bool
+ firmware_debug = bool(unpack(">B", checked_data[2:3])[0])  # bool
```

Copy the two directories to `CIRCUITPY/lib`:

```shell
cp -av CircuitPython_sensirion_i2c_driver/sensirion_i2c_driver CIRCUITPY/lib
cp -av CircuitPython_sensirion_i2c_sen5x/sensirion_i2c_sen5x CIRCUITPY/lib
```

## Test the sensor

Use the provided cable to connect the sensor to the `I2C1` port on the badge.
Refer to the [pinout](https://github.com/makezurich/makezurich-badge-2023/blob/main/makezurich2023-badge-pinout.png) to find the right location on the badge.

Read the address from the back of the Grove All-in-one Environmental Sensor and
set it as the value of the `SEN5X_DEFAULT_ADDRESS` variable in the `main.py` script:

```python
SEN5X_DEFAULT_ADDRESS = 0x69  # The actual address might differ
```

Copy the `main.py` CircuitPython script to `CIRCUITPY`.

The output should be similar to this:

```shell
Product Name: SEN55
Serial Number: 19A2A74224959CE5
Version: Firmware 2.0, Hardware 4.0, Protocol 1.0

Waiting for new data...
Mass Concentration PM1.0:    3.6 µg/m^3
Mass Concentration PM2.5:    4.3 µg/m^3
Mass Concentration PM4.0:    4.8 µg/m^3
Mass Concentration PM10.0:   5.0 µg/m^3
Ambient Humidity:            48.34 %RH
Ambient Temperature:         26.31 °C
VOC Index:                   0.0
NOx Index:                   N/A
Device Status: 0x00000000 [OK]
```
