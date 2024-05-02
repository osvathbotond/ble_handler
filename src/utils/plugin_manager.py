from pkgutil import walk_packages
from importlib import import_module

import receivers
import senders
from receivers._abc import Receiver
from senders._abc import Sender


_RECEIVERS: dict[str, type[Receiver]] = {}
_SENDERS: dict[str, Sender] = {}


# Register
def register_receiver(name: str):
    def decorator(cls):
        _RECEIVERS[name] = cls
        return cls

    return decorator


def register_sender(name: str):
    def decorator(cls):
        _SENDERS[name] = cls()
        return cls

    return decorator


# Get
def get_receiver(name: str) -> type[Receiver]:
    if name in _RECEIVERS:
        return _RECEIVERS[name]
    else:
        options = ", ".join(f'"{k}"' for k in _RECEIVERS)
        raise KeyError(
            f'Receiver "{name}" is not available. Possible options are: {options}.'
        )


def get_sender(name: str) -> Sender:
    if name in _SENDERS:
        return _SENDERS[name]
    else:
        options = ", ".join(f'"{k}"' for k in _SENDERS)
        raise KeyError(f'Sender "{name}" is not available. Possible options: {options}')


def get_receivers() -> dict[str, type[Receiver]]:
    return _RECEIVERS


def get_senders() -> dict[str, Sender]:
    return _SENDERS


# Load
def load_receivers() -> None:
    for _, name, _ in walk_packages(receivers.__path__, f"{receivers.__name__}."):
        try:
            import_module(name)
        except Exception as err:
            print(f'Could not load module "{name}": {err!r}')


def load_senders() -> None:
    for _, name, _ in walk_packages(senders.__path__, f"{senders.__name__}."):
        try:
            import_module(name)
        except Exception as err:
            print(f'Could not load module "{name}": {err!r}')


# Setup
def setup_senders(config: dict) -> None:
    for sender_name, sender in _SENDERS.items():
        if hasattr(sender, "setup") and sender_name in config:
            sender.setup(config[sender_name])


# Teardown
def teardown_senders() -> None:
    for _, sender in _SENDERS.items():
        if hasattr(sender, "teardown"):
            sender.teardown()
