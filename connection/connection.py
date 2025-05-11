from bleak import BleakClient, BleakScanner
from .uart import UartService
from btooth import BluetoothDevice, BluetoothEventLoop, ThreadEventLoop

class Connection:
    def __init__(self, address_or_bluetoothdevice):
        if isinstance(address_or_bluetoothdevice, BluetoothDevice):
            self._device = address_or_bluetoothdevice
        else:
            self._device = BluetoothDevice(BleakClient(address_or_bluetoothdevice))
        self.uart = UartService(self._device)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    def connect(self) -> None:
        self._device.connect()

    def disconnect(self) -> None:
        self._device.disconnect()

    @staticmethod
    def find_microbit(microbit_name: str = None, timeout: int = 3, loop: BluetoothEventLoop = None) -> 'Connection':
        loop = loop if loop else ThreadEventLoop.single_thread()

        def name_filter(d, ad):
            return Connection._name_filter(microbit_name)(ad.local_name)

        device = loop.run_async(BleakScanner.find_device_by_filter(filterfunc=name_filter, timeout=timeout)).result()
        if device:
            return Connection(BluetoothDevice(BleakClient(device), loop))
        else:
            raise Exception(f"No device with name {microbit_name} found.")

    @staticmethod
    def _name_filter(microbit_name: str = None):
        return lambda \
            device_name: device_name == f'BBC micro:bit [{microbit_name.strip()}]' \
            if microbit_name \
            else device_name and device_name.startswith('BBC micro:bit')
