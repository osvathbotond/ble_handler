from functools import partial
from typing import Callable

from utils.plugin_manager import get_sender
from utils.plugin_manager import get_receiver
from receivers._abc import Receiver


class Device:
    def __init__(self, mac: str, config: dict) -> None:
        self.mac: str = mac
        self.receiver: type[Receiver] = get_receiver(config["receiver"])
        self.receiver_name: str = config["receiver"]
        self.sender_configs: dict = config["senders"]

        self.senders: list[Callable[[Receiver], None]] = [
            partial(get_sender(sender).send_message, config["name"], settings)
            for sender, settings in self.sender_configs.items()
        ]
