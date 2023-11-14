from senders._abc import Sender
from receivers._abc import Receiver
from utils.plugin_manager import register_sender

@register_sender("print")
class PrintSender(Sender):
    def setup(self, _: dict) -> None:
        return
    
    def teardown(self) -> None:
        return
    
    def send_message(self, name: str, _: dict, receiver: Receiver) -> None:
        print(receiver.to_json(name), flush=True)
