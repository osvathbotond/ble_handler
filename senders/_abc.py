from abc import ABC
from abc import abstractmethod

from receivers._abc import Receiver

class Sender(ABC):
    @abstractmethod
    def setup(self, config: dict) -> None:
        ...
    
    @abstractmethod
    def teardown(self) -> None:
        ...
    
    @abstractmethod
    def send_message(self, name: str, settings: dict, receiver: Receiver) -> None:
        ...