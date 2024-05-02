from __future__ import annotations
from abc import ABC
from abc import abstractmethod


class Receiver(ABC):
    @abstractmethod
    def to_json(self, name: str) -> dict: ...

    @staticmethod
    @abstractmethod
    def check_type(message: bytes) -> bool: ...

    @staticmethod
    @abstractmethod
    def from_message(cls, message: bytes) -> Receiver: ...
