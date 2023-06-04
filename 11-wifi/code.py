import os
import ssl
import time
import wifi
import socketpool
import adafruit_requests as requests

# Requirements:
# - lib/adafruit_requests.py
# More information at https://learn.adafruit.com/pico-w-wifi-with-circuitpython

# Load WiFi details from settings.toml
bit_ssid = os.getenv('CIRCUITPY_WIFI_SSID_BIT')
bit_password = os.getenv('CIRCUITPY_WIFI_PASSWORD_BIT')
ewz_ssid = os.getenv('CIRCUITPY_WIFI_SSID_EWZ')
ewz_password = os.getenv('CIRCUITPY_WIFI_PASSWORD_EWZ')

# Scan for networks:
connected_wifi_ssid = None
networks = wifi.radio.start_scanning_networks()
while not wifi.radio.connected:
    print("Scanning for WiFi networks...")
    time.sleep(3)
    print("Found the following WiFi networks (will break once known network found):")
    for network in networks:
        print(f"- {network.ssid}")
        if network.ssid == bit_ssid:
            print(f"Connecting to {network.ssid}...")
            try:
                wifi.radio.connect(network.ssid, bit_password)
            except ConnectionError:
                print(f"Unable to connect to {network.ssid}")
            if wifi.radio.connected:
                connected_wifi_ssid = network.ssid
                break
        if network.ssid == ewz_ssid:
            print(f"Connecting to {network.ssid}...")
            try:
                wifi.radio.connect(network.ssid, ewz_password)
            except ConnectionError:
                print(f"Unable to connect to {network.ssid}")
            if wifi.radio.connected:
                connected_wifi_ssid = network.ssid
                break

wifi.radio.stop_scanning_networks()

# Mind that the badge will remain connected to the last connected network
# and display "None" if it has already been connected before.
# You need to reset the badge to connect to a different network.
if not connected_wifi_ssid:
    print("Connected to one of the known WiFi networks.")
else:
    print(f"Connected to WiFi network: {connected_wifi_ssid}")
print(f"IP address: {wifi.radio.ipv4_address}")

# Make a request to httpbin.org
pool = socketpool.SocketPool(wifi.radio)
requests = requests.Session(pool, ssl.create_default_context())
api_url = "https://httpbin.org/anything"
response = requests.get(api_url)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Something went wrong connecting to {api_url}")
response.close()

# To (maybe) reduce battery consumption, close all sockets
wifi.radio.enabled = False
print("Closed all sockets.")
