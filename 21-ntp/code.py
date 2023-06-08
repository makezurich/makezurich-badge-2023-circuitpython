import wifi
import adafruit_ntp
import time
import os
import socketpool

# Requirements:
# - lib/adafruit_ntp.mpy

# Load WiFi details from settings.toml
WIFI_SSID = os.getenv('CIRCUITPY_WIFI_SSID')
WIFI_PASS = os.getenv('CIRCUITPY_WIFI_PASSWORD')

print("Connecting to Wi-Fi \"{0}\"...".format(WIFI_SSID))
wifi.radio.connect(WIFI_SSID, WIFI_PASS) # waits for IP address
print("Connected, IP address = {0}".format(wifi.radio.ipv4_address))

tz_offset = 2
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset = tz_offset)

def struct_time_to_iso(t):
    time = '{0}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}'.format(*t)
    return '{0}+0{1}:00'.format(time, tz_offset)

while True:
    now_iso = struct_time_to_iso(ntp.datetime)
    print(now_iso)
    time.sleep(1)
