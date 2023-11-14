from bluetooth._bluetooth import hci_open_dev
from threading import Thread
from threading import Event
from time import sleep

from utils.bluetooth_utils import enable_le_scan
from utils.bluetooth_utils import parse_le_advertising_events
from utils.plugin_manager import load_receivers
from utils.plugin_manager import get_receivers


def le_advertise_packet_handler(mac, _, data, _):
    if mac not in devices:
        for name, receiver in receivers.items():
            if receiver.check_type(data[4:]):
                devices[mac] = name

def log():
    while True:
        for _ in range(10):
            sleep(1)
            if stop_event.is_set():
                return
        print(devices)

if __name__ == "__main__":
    stop_event = Event()
    devices = {}

    load_receivers()

    sock = hci_open_dev(0)
    enable_le_scan(sock, filter_duplicates=False)

    receivers = get_receivers()

    thread_bt = Thread(target=parse_le_advertising_events, kwargs={"sock": sock, "handler": le_advertise_packet_handler, "debug": False})
    thread_bt.start()
    thread_log = Thread(target=log)
    thread_log.start()
    
    try:
        thread_bt.join()
    except KeyboardInterrupt:
        stop_event.set()
