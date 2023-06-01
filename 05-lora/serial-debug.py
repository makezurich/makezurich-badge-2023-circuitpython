import board
import busio
import digitalio
import time
import supervisor

uart = busio.UART(board.GP4, board.GP5, baudrate=9600)
get_input = True
message_started = False
message_print = []
allstring = ""
printshow = False

while True:
    if supervisor.runtime.serial_bytes_available:
        allstring=""
        # wait for user input
        userinput = input().strip() #input command
        userinput = userinput + "\n"
        # convert to byte
        b = bytes(userinput, 'utf-8')
        # write out the byte
        print("sending: " + userinput)
        uart.write(b)
        continue
    byte_read = uart.readline()# read one line
    if byte_read != None:
        allstring += byte_read.decode()
        printshow = True
    else:
        if printshow == True:
            if allstring != "":
                print(allstring)
            allstring=""
            printshow ==False
