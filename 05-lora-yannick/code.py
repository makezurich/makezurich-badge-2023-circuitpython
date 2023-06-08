# This example packages the data into a bytearray with python struct
# In ttn_payload_formatter.js we show an example on how to parse it again.
# You can setup the ttn_payload_formatter.js in the TTN console

# hardware: https://www.seeedstudio.com/LoRa-E5-Wireless-Module-p-4745.html
# AT Commands https://files.seeedstudio.com/products/317990687/res/LoRa-E5%20AT%20Command%20Specification_V1.0%20.pdf
# TODO(yw): parse AT command response correctly

import board
import busio
import digitalio
import time
import binascii
import struct

uart = busio.UART(board.GP4, board.GP5, baudrate=9600, timeout=20)

def at_send(cmd, max_time=10):
    if not isinstance(cmd, bytes):
        print("cmd must be a byte string, terminated with new line")
        return ""

    now = time.monotonic()
    uart.write(cmd)
    result = ""
    while True:
        byte_read = uart.readline() # read one line
        if byte_read == None: # no more response
            break

        response = byte_read.decode()
        result += response
        if (time.monotonic() - now) > max_time:
            print("reached at_send max_time", max_time)
            break

    return result

# return dict with the ids
def lora_get_ids():
    response = at_send(b"AT+ID\n")
    result = {
        "DevAddr": "",
        "DevEui": "",
        "AppEui": "",
    }
    for line in response.splitlines():
        for key in result.keys():
            if key in line:
                result[key] = line.split(",")[1].strip()

    return result

# LWOTAA or LWABP (we recommend LWOTAA)
def lora_get_mode():
    result_string = at_send(b"AT+MODE\n")
    return result_string.split(":")[1].strip()

def lora_get_datarate():
    result_string = at_send(b"AT+DR\n")
    return result_string

def lora_set_datarate():
    # TODO(yw): should accept
    result_string = at_send(b"AT+DR=5\n")
    return result_string

def lora_join():
    result_string = at_send(b"AT+JOIN\n", 10)
    return result_string

def lora_set_appkey(appkey):
    result_string = at_send(b"AT+KEY=APPKEY," + appkey + "\n", 10)
    return result_string

def lora_send_text(msg):
    """Function to send data, waits for confirmation
    :param msg: data to send, can be string or bytes
    """
    payload = b""
    downstream_messages = []
    if isinstance(msg, str):
        userinput = msg.strip()
        payload = bytes(userinput, "utf-8")
    else:
        print("Please provide a string")
        return

    cmd = b"AT+CMSG=" + payload + b"\n"
    response = at_send(cmd, 10)
    # TODO(yw): check for ": Done"
    return response

def lora_send_hex(msg):
    """Function to send data, waits for confirmation
    :param msg: data to send, can be string or bytes
    """
    payload = b""
    downstream_messages = []
    if isinstance(msg, str):
        userinput = msg.strip()
        payload = bytes(userinput, "utf-8")
    else:
        payload = msg

    payload = binascii.hexlify(payload)

    cmd = b"AT+CMSGHEX=" + payload + b"\n"
    response = at_send(cmd, 10)
    # TODO(yw): check for ": Done"
    return response

print("LoRa IDs:", lora_get_ids())

# Setting the LoRa Appkey is only required once, will be stored
# print(lora_set_appkey(b"APP_KEY_FROM_THINGS_CONSOLE"))

# Setting the LoRa datarate is only required once, will be stored
# print(lora_set_datarate())

result = lora_join()
print(result)

DEVICE_HEALTHY = 0
DEVICE_LOW_BATTERY = 1
DEVICE_ERROR = 2

device_state = DEVICE_HEALTHY
latitude = 47.401330503492595
longitute = 8.390119229678902
temperature = 25.4 # °C
humidity = 25 # %
co2_ppm = 1240

# struct.pack pattern
# <: little endian
# >: big endian
# b: signed char, 1byte
# B: unsigned signed char, 1byte 0-255
# ?: boolean, 1byte 0-1
# h: short, 2byte
# i: int, 4byte
# I: unsigned int, 4byte
# l: long, 8byte
# f: float, 4byte
# d: double, 8byte
# q: long long int, 8byte
# Q: unsigned long long, 8byte
buffer = struct.pack('>bfffbi', device_state, latitude, longitute, temperature, humidity, co2_ppm)
print("sending", binascii.hexlify(buffer))

response = lora_send_hex(buffer)
print(response)

# response = lora_send_text("hello world")
# print(response)

print("finishd")

time.sleep(2)
