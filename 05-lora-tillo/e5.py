import time


class LoRaModule:
    def __init__(self, uart) -> None:
        self.uart = uart

    def show_information(self) -> None:
        self.at_send("AT+CH")
        self.at_send("AT+MODE")
        self.at_send("AT+ID")

    def set_mode(self, mode) -> None:
        if self.get_mode() != mode:
            self.at_send(f"AT+MODE={mode}")

    def get_mode(self) -> str:
        result = self.at_send("AT+MODE")
        return result.split(":")[1].strip()

    def get_ids(self) -> dict[str, str]:
        response = self.at_send("AT+ID")
        result = dict(DevAddr="", DevEui="", AppEui="")
        for line in response.splitlines():
            for key in result.keys():
                if key in line:
                    result[key] = line.split(",")[1].strip()

        return result

    def get_data_rate(self) -> str:
        result = self.at_send("AT+DR")
        return result.split(":")[1].strip()

    def set_data_rate(self, data_rate) -> None:
        self.at_send(f"AT+DR={data_rate}")

    def set_appkey(self, appkey) -> None:
        self.at_send(f"AT+KEY=APPKEY, {appkey}")

    def set_appeui(self, appeui) -> None:
        self.at_send(f"AT+ID=APPEUI, {appeui}")

    def setup_and_join_otaa(self, appkey, appeui, force=False) -> bool:
        if force or not self.join():
            self.set_mode("LWOTAA")
            self.set_appkey(appkey)
            self.set_appeui(appeui)

        return self.join()

    def join(self) -> bool:
        result = self.at_send("AT+JOIN", ["+JOIN: Done", "+JOIN: Joined already"])
        if "Joined already" in result:
            return True
        if "failed" in result:
            return False
        else:
            return True

    def send(self, mode, data) -> str:
        return self.at_send(f"AT+{mode}={data}", f"+{mode}: Done")

    def send_hex(self, data) -> str:
        return self.send("MSGHEX", data)

    def send_string(self, data) -> str:
        return self.send("MSG", data)

    def send_confirmed_hex(self, data) -> str:
        return self.send("CMSGHEX", data)

    def send_confirmed_string(self, data) -> str:
        return self.send("CMSG", data)

    def at_send(self, cmd, read_until_condition=None) -> str:
        print(f"--> {cmd}")
        self.uart.write(bytes(cmd + "\n", "utf-8"))
        result = ""
        while True:
            data = self.uart.readline()
            if data is None and not read_until_condition:
                break
            if data is None and read_until_condition:
                time.sleep(0.1)
                continue

            # convert bytearray to string
            data_string = "".join([chr(b) for b in data])
            print(f"<-- {data_string}", end="")
            result += data_string
            if read_until_condition and data_string.strip() in read_until_condition:
                break

        return result

    def factory_reset(self) -> None:
        self.at_send("AT+FDEFAULT")
