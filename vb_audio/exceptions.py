class StreamNeverOpened(Exception):
    def __init__(self):
        super().__init__("Stream was never opened, ensure `VbCableAudio.open()` is called before closing")


class DeviceNotFound(Exception):
    def __init__(self, device_name: str):
        super().__init__("device not found: {}".format(device_name))


class NoCableFound(Exception):
    def __init__(self):
        super().__init__("No cable found")
