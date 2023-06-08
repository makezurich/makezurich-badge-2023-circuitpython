# https://www.cytron.io/tutorial/display-covid-19-data-using-maker-pi-pico-and-circuitpython
# https://gist.github.com/idriszmy/4cad5f2780d7da4c2ff76ac8f6f83565
# https://gist.github.com/idriszmy/4cad5f2780d7da4c2ff76ac8f6f83565#file-grove_lcd_i2c-py
# https://github.com/Seeed-Studio/Grove_LCD_RGB_Backlight/blob/master/rgb_lcd.h

import time
from adafruit_bus_device.i2c_device import I2CDevice

# Command values
LCD_CLEAR_DISPLAY = 0x01
LCD_RETURN_HOME = 0x02
LCD_ENTRY_MODE_SET = 0x04
LCD_DISPLAY_CONTROL = 0x08
LCD_CURSOR_SHIFT = 0x10
LCD_FUNCTION_SET = 0x20
LCD_SET_CG_RAM_ADDR = 0x40
LCD_SET_DD_RAM_ADDR = 0x80

# Flags for display entry mode
LCD_ENTRY_RIGHT = 0x00
LCD_ENTRY_LEFT = 0x02
LCD_ENTRY_SHIFT_INCREMENT = 0x01
LCD_ENTRY_SHIFT_DECREMENT = 0x00

# Flags for display on/off control
LCD_DISPLAY_ON = 0x04
LCD_DISPLAY_OFF = 0x00
LCD_CURSOR_ON = 0x02
LCD_CURSOR_OFF = 0x00
LCD_BLINK_ON = 0x01
LCD_BLINK_OFF = 0x00

# Flags for display/cursor shift
LCD_DISPLAY_MOVE = 0x08
LCD_CURSOR_MOVE = 0x00
LCD_MOVE_RIGHT = 0x04
LCD_MOVE_LEFT = 0x00

# Flags for function set
LCD_8_BIT_MODE = 0x10
LCD_4_BIT_MODE = 0x00
LCD_2_LINE = 0x08
LCD_1_LINE = 0x00
LCD_5x10_DOTS = 0x04
LCD_5x8_DOTS = 0x00


class Grove_LCD_I2C:
    def __init__(self, i2c_bus, lcd_address, cols=16, lines=2, dotsize=LCD_5x8_DOTS):
        self.lcd = I2CDevice(i2c_bus, lcd_address)

        self._displayfunction = 0
        self._displaycontrol = 0
        self._displaymode = 0
        self._initialized = 0
        self._numlines = lines
        self._currline = 0

        if lines > 1:
            self._displayfunction |= LCD_2_LINE
        if (not dotsize == LCD_5x8_DOTS) and lines == 1:
            self._displayfunction |= LCD_5x10_DOTS

        time.sleep(0.05)

        self.command(LCD_FUNCTION_SET | self._displayfunction)
        time.sleep(0.0045)  # wait more than 4.1 ms

        self.command(LCD_FUNCTION_SET | self._displayfunction)
        time.sleep(0.00015)

        self.command(LCD_FUNCTION_SET | self._displayfunction)
        self.command(LCD_FUNCTION_SET | self._displayfunction)

        self._displaycontrol = LCD_DISPLAY_ON | LCD_CURSOR_OFF | LCD_BLINK_OFF
        self.display()
        self.clear()
        self._displaymode = LCD_ENTRY_LEFT | LCD_ENTRY_SHIFT_DECREMENT
        self.command(LCD_ENTRY_MODE_SET | self._displaymode)

    def clear(self):
        self.command(LCD_CLEAR_DISPLAY)
        time.sleep(0.002)

    def home(self):
        self.command(LCD_RETURN_HOME)
        time.sleep(0.002)

    def cursor_position(self, col, row):
        position = col | 0x80 if row == 0 else col | 0xC0
        data = bytearray(2)
        data[0] = 0x80
        data[1] = position
        # print(data)
        self.i2c_send_bytes(data)

    def noDisplay(self):
        self._displaycontrol &= 0xFF - LCD_DISPLAY_ON
        self.command(LCD_DISPLAY_CONTROL | self._displaycontrol)

    def display(self):
        self._displaycontrol |= LCD_DISPLAY_ON
        self.command(LCD_DISPLAY_CONTROL | self._displaycontrol)

    def noCursor(self):
        self._displaycontrol &= 0xFF - LCD_CURSOR_ON
        self.command(LCD_DISPLAY_CONTROL | self._displaycontrol)

    def cursor(self):
        self._displaycontrol &= 0xFF - LCD_CURSOR_ON
        self.command(LCD_DISPLAY_CONTROL | self._displaycontrol)

    def noBlink(self):
        self._displaycontrol |= LCD_CURSOR_ON
        self.command(LCD_DISPLAY_CONTROL | self._displaycontrol)

    def blink(self):
        self._displaycontrol |= LCD_BLINK_ON
        self.command(LCD_DISPLAY_CONTROL | self._displaycontrol)

    def scrollDisplayLeft(self):
        self.command(LCD_CURSOR_SHIFT | LCD_DISPLAY_MOVE | LCD_MOVE_LEFT)

    def scrollDisplayRight(self):
        self.command(LCD_CURSOR_SHIFT | LCD_DISPLAY_MOVE | LCD_MOVE_RIGHT)

    def rightToLeft(self):
        self._displaymode |= LCD_ENTRY_LEFT
        self.command(LCD_ENTRY_MODE_SET | self._displaymode)

    def autoscroll(self):
        self._displaymode |= LCD_ENTRY_SHIFT_INCREMENT
        self.command(LCD_ENTRY_MODE_SET | self._displaymode)

    def noAutoscroll(self):
        self._displaymode &= 0xFF - LCD_ENTRY_SHIFT_INCREMENT
        self.command(LCD_ENTRY_MODE_SET | self._displaymode)

    def createChar(self, location, charmap):
        location &= 0x7
        self.command(LCD_SET_CG_RAM_ADDR | (location << 3))
        data = bytearray(9)
        data[0] = 0x40
        for i in range(8):
            data[i + 1] = charmap[i]
        self.i2c_send_bytes(data)

    def command(self, value):
        data = bytearray(2)
        data[0] = 0x80  # command register address
        data[1] = value  # command byte
        self.i2c_send_bytes(data)

    def write(self, value):
        data = bytearray(2)
        data[0] = 0x40
        data[1] = value
        self.i2c_send_bytes(data)
        return 1

    def i2c_send_bytes(self, data):
        with self.lcd as wire:
            wire.write(data)

    def print(self, text):
        string = str(text)
        for char in string:
            if char == "\n":
                self.cursor_position(0, 1)
            else:
                self.write(ord(char))
