PDU_BYTE_LIMIT = 20
UART = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
TX_CHARACTERISTIC = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
RX_CHARACTERISTIC = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'

class UartService:
    def __init__(self, device):
        self._device = device

    def receive(self, callback):
        self._device.notify(UART, TX_CHARACTERISTIC, lambda sender, data: callback(data))

    def receive_string(self, callback):
        self.receive(UartService.to_string(callback))

    def send(self, data):
        for i in range(0, len(data), PDU_BYTE_LIMIT):
            self._device.write(UART, RX_CHARACTERISTIC, data[i:i + PDU_BYTE_LIMIT])

    def send_string(self, string):
        self.send(UartService.from_string(string))

    @staticmethod
    def from_string(string):
        return string.encode("utf-8")

    @staticmethod
    def to_string(callback):
        return lambda data: callback(str(data, "utf-8"))
