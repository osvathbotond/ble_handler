import json
import paho.mqtt.client as mqtt

from senders._abc import Sender
from receivers._abc import Receiver
from utils.plugin_manager import register_sender

@register_sender("mqtt")
class MqttSender(Sender):
    def setup(self, config: dict) -> None:
        address = config["address"]
        port = config["port"]

        self.client = mqtt.Client()
        self.client.connect(address, port)

    def teardown(self) -> None:
        self.client.disconnect()
    
    def send_message(self, name: str, settings: dict, receiver: Receiver) -> None:
        self.client.publish(settings["topic"], json.dumps(receiver.to_json(name)))
