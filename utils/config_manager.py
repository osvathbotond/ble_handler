import json

from utils.device import Device


class Config:
    def __init__(self, path) -> None:
        with open(path) as f:
            self.config = json.load(f)

    def get_devices(self):
        self.devices = {mac: Device(mac, subconfig) for mac, subconfig in self.config["devices"].items()}

        return self.devices
