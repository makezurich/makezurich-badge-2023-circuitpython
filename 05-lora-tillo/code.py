import board
import busio
import e5

mode = 'OTAA'
appkey = 'your appkey'
appeui = 'your appeiu'

#Set UART Pins

uart = busio.UART(board.GP4, board.GP5, baudrate=9600)
lora_module = e5.LoRa_module(uart)

lora_module.show_information()
lora_module.setup_and_join(mode, appkey, appeui)

lora_module.send('MSGHEX','01234567')
