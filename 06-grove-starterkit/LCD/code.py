# offical example is micropython https://wiki.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico/#software-4
# datasheet https://github.com/SeeedDocument/Grove-16x2_LCD_Series/raw/master/res/JDH_1804_Datasheet.pdf
# product page https://www.seeedstudio.com/Grove-16x2-LCD-White-on-Blue.html

# i2c address is 0x3e

import board
import busio

lcd_addr=0x3E

i2c = busio.I2C(board.GP3, board.GP2)

# TODO(yw): implement
