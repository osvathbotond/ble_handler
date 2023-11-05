from abc import ABC
from abc import abstractmethod
from abc import abstractstaticmethod
from abc import abstractclassmethod

class Receiver(ABC):
    @abstractmethod
    def to_json(self, name: str) -> dict:
        ...

    @abstractstaticmethod
    def check_type(message: bytes) -> bool:
        ...

    @abstractclassmethod
    def from_message(cls, message: bytes):
        ...
