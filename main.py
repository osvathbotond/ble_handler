from bluetooth._bluetooth import hci_open_dev
from os.path import join
from os.path import dirname

from utils.plugin_manager import load_senders
from utils.plugin_manager import load_receivers
from utils.plugin_manager import setup_senders
from utils.plugin_manager import teardown_senders
from utils.config_manager import Config
from utils.bluetooth_utils import enable_le_scan
from utils.bluetooth_utils import parse_le_advertising_events


def le_advertise_packet_handler(mac, _, data, _):
    dev = devices[mac]
    res = dev.receiver.from_message(data[4:])
    for sender in dev.senders:
        sender(res)

if __name__ == "__main__":
    load_senders()
    load_receivers()

    config_path = join(dirname(__file__), "config.json")
    config = Config(config_path)
    devices = config.get_devices()

    setup_senders(config.config["senders"])

    sock = hci_open_dev(0)
    enable_le_scan(sock, filter_duplicates=False)
    
    try:
        parse_le_advertising_events(sock=sock, mac_addr=devices.keys(), handler=le_advertise_packet_handler, debug=False)
    except KeyboardInterrupt:
        teardown_senders()