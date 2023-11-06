import pkgutil
import importlib

import receivers
import senders


_RECEIVERS = {}
_SENDERS = {}


# Register
def register_receiver(name):
    def decorator(cls):
        _RECEIVERS[name] = cls
        return cls
    return decorator

def register_sender(name):
    def decorator(cls):
        _SENDERS[name] = cls()
        return cls
    return decorator

# Get
def get_receiver(name):
    if name in _RECEIVERS:
        return _RECEIVERS[name]
    else:
        options = ", ".join(f"\"{k}\"" for k in _RECEIVERS)
        raise KeyError(f"Receiver \"{name}\" is not available. Possible options are: {options}.")

def get_sender(name):
    if name in _SENDERS:
        return _SENDERS[name]
    else:
        options = ", ".join(f"\"{k}\"" for k in _SENDERS)
        raise KeyError(f"Sender \"{name}\" is not available. Possible options: {options}")

def get_receivers():
    return _RECEIVERS

def get_senders():
    return _SENDERS

# Load
def load_receivers():
    for _, name, _ in pkgutil.walk_packages(receivers.__path__, f"{receivers.__name__}."):
        try:
            importlib.import_module(name)
        except Exception as err:
            print(f"Could not load module \"{name}\": {err!r}")

def load_senders():
    for _, name, _ in pkgutil.walk_packages(senders.__path__, f"{senders.__name__}."):
        try:
            importlib.import_module(name)
        except Exception as err:
            print(f"Could not load module \"{name}\": {err!r}")

# Setup
def setup_senders(config):
    for sender_name, sender in _SENDERS.items():
        if hasattr(sender, "setup") and sender_name in config:
            sender.setup(config[sender_name])

# Teardown
def teardown_senders():
    for sender_name, sender in _SENDERS.items():
        if hasattr(sender, "teardown"):
            sender.teardown()