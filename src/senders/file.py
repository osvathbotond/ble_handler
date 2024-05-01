import json

from senders._abc import Sender
from receivers._abc import Receiver
from utils.plugin_manager import register_sender


@register_sender("file")
class FileSender(Sender):
    def setup(self, _: dict) -> None:
        self.files = {}

    def teardown(self) -> None:
        for file in self.files.values():
            file.close()

    def send_message(self, name: str, settings: dict, receiver: Receiver) -> None:
        fn = settings["filename"]
        if fn not in self.files:
            self.files[fn] = open(fn, "a")

        file = self.files[fn]
        file.write(f"{json.dumps(receiver.to_json(name))}\n")
