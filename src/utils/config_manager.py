import json

from utils.device import Device


class Config:
    def __init__(self, path: str) -> None:
        with open(path) as f:
            self.config = json.load(f)

    def get_devices(self) -> dict[str, Device]:
        self.devices = {
            mac: Device(mac, subconfig)
            for mac, subconfig in self.config["devices"].items()
        }

        return self.devices
