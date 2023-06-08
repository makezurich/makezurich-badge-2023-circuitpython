# GPS with ublox: PAM7Q
# from https://github.com/adafruit/Adafruit_CircuitPython_GPS
# https://www.u-blox.com/en/product/pam-7q-module
# https://content.u-blox.com/sites/default/files/PAM-7Q_DataSheet_%28UBX-13002455%29.pdf

# Top side with shield (metall part is bottom)
# |              |
# |---------------
# 1 2 3 4 5 6 7 8
#
# 1: Serial RXD
# 2: Serial TXD
# 3: GND (Ground)
# 4: VCC 3.3v (Supply voltage)
# 5: V_BCKP (Backup voltage supply)
# 6: TIMEPULSE Time pulse (1 Hz nav clock output)

import time
import board
import busio
import adafruit_gps

uart = busio.UART(board.GP0, board.GP1, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()
while True:
    gps.update()

    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print('Waiting for fix...') # make sure you are under the sky
            continue
        print('=' * 40) # Print a separator line.
        print('Latitude: {0:.6f} degrees'.format(gps.latitude))
        print('Longitude: {0:.6f} degrees'.format(gps.longitude))
