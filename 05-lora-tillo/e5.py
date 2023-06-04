import time

class LoRa_module:

    def __init__(self,uart) -> None:
        self.uart = uart

    def show_information(self):
        self.send_and_recv('AT+CH')
        self.send_and_recv('AT+MODE')
        self.send_and_recv('AT+ID')

    def set_mode(self,mode):
        self.send_and_recv(f'AT+MODE={mode}')

    def setup_and_join(self, mode, appkey, appeui) -> bool:
        self.set_mode(mode)
        self.send_and_recv(f'AT+KEY=APPKEY, {appkey}')
        self.send_and_recv(f'AT+ID=APPEUI, {appeui}')
        return self.join()

    def join(self) -> bool:
        self.send_and_recv('AT+JOIN')
        data = self.uart.readline()
        while data is  None:
            time.sleep(.2)
            data = self.uart.readline()
        data_string = ''.join([chr(b) for b in data])
        print(f'<-- {data_string}', end="")
        if "failed" in data_string:
            return False
        else:
            return True

    def send(self, mode,data):
        self.send_and_recv(f'AT+{mode}={data}')
        while data is  None:
            time.sleep(.2)
            data = self.uart.readline()
        print(f'Sent: {data}')

    def send_and_recv(self,cmd):
        print(f'--> {cmd}')
        self.uart.write(bytes(cmd,'utf-8'))
        data = self.uart.readline()
        while data is not None:
            # convert bytearray to string
            data_string = ''.join([chr(b) for b in data])
            print(f'<-- {data_string}', end="")
            data = self.uart.readline()
