# Example on how to connect to Wi-Fi and MQTT.
# Publishes temperature and device id to the users MQTT namespace.

import binascii
import ssl
import time
from random import randint
from adafruit_datetime import datetime
import adafruit_minimqtt.adafruit_minimqtt as minimqtt
import microcontroller
import socketpool
import wifi

WIFI_SSID = "Wifi-name"
WIFI_PASS = "wifi-password"

device_uid = binascii.hexlify(microcontroller.cpu.uid).decode("utf-8")

MQTT_HOST = "192.168.1.XXX"
MQTT_PORT = 1883
MQTT_USERNAME = "john.doe"
MQTT_PASSWORD = "mqtt-password"
MQTT_CLIENT_ID = 'badge_' + MQTT_USERNAME

user_id = MQTT_USERNAME

print("Connecting to Wi-Fi \"{0}\"...".format(WIFI_SSID))
wifi.radio.connect(WIFI_SSID, WIFI_PASS) # waits for IP address
print("Connected, IP address = {0}".format(wifi.radio.ipv4_address))

pool = socketpool.SocketPool(wifi.radio)
context = ssl.create_default_context()

def handle_connect(client, userdata, flags, rc):
    print("Connected to {0}".format(client.broker))
    mqtt_client.subscribe("/userA/qrcode") # check if this is right time to sub

def handle_publish(client, userdata, topic, pid):
    pass
    #print("Published to {0}".format(topic))

def handle_message(client, topic, message):
    # Method called when a client's subscribed feed has a new value.
    print("New message on topic {0}: {1}".format(topic, message))

def handle_subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

mqtt_client = minimqtt.MQTT(
    broker = MQTT_HOST,
    port = MQTT_PORT,
    client_id = MQTT_CLIENT_ID,
    username = MQTT_USERNAME,
    password = MQTT_PASSWORD,
    socket_pool = pool,
    ssl_context = context)

mqtt_client.on_connect = handle_connect
mqtt_client.on_publish = handle_publish
mqtt_client.on_subscribe = handle_subscribe
mqtt_client.on_message = handle_message

print("\nConnecting to {0}...".format(MQTT_HOST))
mqtt_client.connect()
mqtt_client.publish(f"/{user_id}/deviceID", device_uid)

# TODO: handle publish errors

while True:
    # MQTT publish: temperature
    t = microcontroller.cpu.temperature
    # print("{:.2f}".format(t) + "c")
    mqtt_client.publish(f"/{user_id}/temperature", "{:.2f}".format(t))

    mqtt_client.loop()
    time.sleep(5)
