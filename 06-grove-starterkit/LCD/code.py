# Official example in micropython: https://wiki.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico/#software-4
# Datasheet: https://github.com/SeeedDocument/Grove-16x2_LCD_Series/raw/master/res/JDH_1804_Datasheet.pdf
# Product page: https://www.seeedstudio.com/Grove-16x2-LCD-White-on-Blue.html
# https://gist.github.com/shahrulnizam/9dc64fe0900b67c85610aaf2880f6bcf#file-circuitpython-lesson-grove-lcd

import time
import board
import busio

from grove_lcd_i2c import Grove_LCD_I2C

LCD_SCL = board.GP3
LCD_SDA = board.GP2
LCD_ADDR = 0x3E

i2c = busio.I2C(scl=LCD_SCL, sda=LCD_SDA)
lcd = Grove_LCD_I2C(i2c, LCD_ADDR)

while True:
    lcd.clear()
    lcd.cursor_position(0, 0)
    lcd.print("Hello MakeZurich!")
    for i in range(1000):
        lcd.cursor_position(0, 1)
        lcd.print(i)
    time.sleep(1)

    lcd.clear()
    lcd.cursor_position(16, 1)
    lcd.autoscroll()
    for i in range(10):
        lcd.print(i)
        time.sleep(0.5)
    lcd.noAutoscroll()
    time.sleep(1)

    lcd.clear()
    lcd.cursor_position(0, 0)
    lcd.print(" Welcome to")
    lcd.cursor_position(0, 1)
    lcd.print("MakeZurich.ch")
    time.sleep(1)

    for i in range(15):
        lcd.scrollDisplayRight()
        time.sleep(0.5)
    for i in range(15):
        lcd.scrollDisplayLeft()
        time.sleep(0.5)
