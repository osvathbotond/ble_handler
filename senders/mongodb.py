from pymongo import MongoClient

from senders._abc import Sender
from receivers._abc import Receiver
from utils.plugin_manager import register_sender

@register_sender("mongodb")
class MongoDBSender(Sender):
    def setup(self, config: dict) -> None:
        address = config["address"]
        port = config["port"]
        username = config["username"]
        password = config["password"]
        database = config["database"]
        collection = config["collection"]

        self.client = MongoClient(f"mongodb://{username}:{password}@{address}:{port}/")
        self.client.start_session()
        self.database = self.client[database]
        self.collection = self.database[collection]

    def teardown(self) -> None:
        return

    def send_message(self, name: str, settings: dict, receiver: Receiver) -> None:
        self.collection.insert_one(receiver.to_json(name))
