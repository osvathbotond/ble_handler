from senders._abc import Sender
from receivers._abc import Receiver
from utils.plugin_manager import register_sender


@register_sender("nothing")
class PrintSender(Sender):
    def setup(self, _: dict) -> None:
        return

    def teardown(self) -> None:
        return

    def send_message(self, _1: str, _2: dict, _3: Receiver) -> None:
        return
