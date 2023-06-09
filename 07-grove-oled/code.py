# Grove - OLED Display 0.66" 64×48 (SSD1306)
# more examples
#  https://github.com/adafruit/Adafruit_CircuitPython_Display_Text
#  https://learn.adafruit.com/circuitpython-display-support-using-displayio/library-overview

# offical docs https://wiki.seeedstudio.com/Grove-OLED-Display-0.66-SSD1306_v1.0/

# !! OLED Display 0.66" (SSD1306) screen is based on the 128×64 resolution screen.
# !! you may need to start the point at (31,16) instead of (0,0). The range is from (31,16) to (95,63)

# requires
# - lib/adafruit_bus_device
# - lib/adafruit_display_text
# - lib/adafruit_displayio_ssd1306.mpy
# - lib/adafruit_ssd1306.mpy

import displayio
import terminalio
import board
import busio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
displayio.release_displays() # release any currently configured displays

i2c = busio.I2C(scl=board.GP1, sda=board.GP0, frequency=400_000)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
WIDTH = 64
HEIGHT = 48
BORDER = 1

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
display.root_group.hidden = True # Disable serial output on the display

# Make the display context, the range is from (31,16) to (95,63).
splash = displayio.Group(x=31, y=16)
display.show(splash)

# Draw a label
text = "Hello\nWorld!"
text_area = label.Label(
    terminalio.FONT, text=text
)
text_area.x = 4
text_area.y = 6
splash.append(text_area)

while True:
    pass
