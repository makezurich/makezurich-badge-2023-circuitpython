import board
import busio
import digitalio
import time

uart = busio.UART(board.GP4, board.GP5, baudrate=9600, timeout=1)

def at_send(cmd, max_time=1):
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

        result += byte_read.decode()
        if (time.monotonic() - now) > max_time:
            print("reached at_send max_time")
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
    result_string = at_send(b"AT+JOIN\n", 5)
    return result_string

def lora_set_key():
    # TODO(yw): parameter
    result_string = at_send(b'AT+KEY=APPKEY,""\n', 1)
    return result_string

# TODO(yw): wait for response, with timeout
def lora_send(msg):
    """Function to send data, waits for confirmation
    :param msg: data to send, can be string or bytes
    """
    payload = b""
    if isinstance(msg, str):
        userinput = msg.strip()
        payload = bytes(userinput, "utf-8")
    else:
        payload = msg

    cmd = b"AT+CMSG=" + payload + b"\n"
    print(cmd)
    result_string = at_send(cmd)
    return result_string

print("LoRa IDs:")
print(lora_get_ids())

#print(lora_set_key())

lora_set_datarate()

result = lora_join()
print(result)
#result = lora_send("hello")
#print(result)

while True:
    pass
