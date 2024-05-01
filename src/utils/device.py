from functools import partial

from utils.plugin_manager import get_sender
from utils.plugin_manager import get_receiver


class Device:
    def __init__(self, mac: str, config: dict) -> None:
        self.mac = mac
        self.receiver = get_receiver(config["receiver"])
        self.receiver_name = config["receiver"]
        self.sender_configs = config["senders"]

        self.senders = [
            partial(get_sender(sender).send_message, config["name"], settings)
            for sender, settings in self.sender_configs.items()
        ]
