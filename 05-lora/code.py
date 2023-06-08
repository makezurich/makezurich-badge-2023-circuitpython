# device details and configuration of app key

import board
import busio
import digitalio
import time

uart = busio.UART(board.GP4, board.GP5, baudrate=9600, timeout=20)

def setup():
    print("LoRa IDs:", lora_get_ids())

    # Setting the LoRa datarate is only required once, will be stored
    print(lora_set_datarate())

    # Setting the LoRa Appkey is only required once, will be stored
    print(lora_set_appkey(b"APP_KEY_FROM_THINGS_CONSOLE"))

    print("finished")

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


setup()
