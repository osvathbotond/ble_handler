from bluetooth._bluetooth import hci_open_dev
from time import sleep
from threading import Thread
from threading import Event
from os.path import join
from os.path import dirname
from argparse import ArgumentParser

from utils.plugin_manager import load_senders
from utils.plugin_manager import load_receivers
from utils.plugin_manager import setup_senders
from utils.plugin_manager import teardown_senders
from utils.plugin_manager import get_receivers
from utils.config_manager import Config
from utils.bluetooth_utils import enable_le_scan
from utils.bluetooth_utils import parse_le_advertising_events
from receivers._abc import Receiver


class Main:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = join(dirname(__file__), "config.json")

        load_senders()
        load_receivers()

        self.config = Config(config_path)
        self.devices = self.config.get_devices()

        setup_senders(self.config.config["senders"])

    def le_advertise_packet_handler(
        self, mac: str, adv_type: int, data: bytes, rssi: int
    ) -> None:
        device = self.devices[mac]
        res = device.receiver.from_message(data[4:])
        for sender in device.senders:
            sender(res)

    def main(self) -> int:
        sock = hci_open_dev(0)
        enable_le_scan(sock, filter_duplicates=False)

        try:
            parse_le_advertising_events(
                sock=sock,
                mac_addr=self.devices.keys(),
                handler=self.le_advertise_packet_handler,
                debug=False,
            )
        except KeyboardInterrupt:
            teardown_senders()

        return 0


class Discover:
    def __init__(self) -> None:
        load_receivers()

        self.devices: dict[str, str] = {}
        self.receivers: dict[str, type[Receiver]] = get_receivers()
        self.stop_event: Event = Event()

    def le_advertise_packet_handler(
        self, mac: str, adv_type: int, data: bytes, rssi: int
    ) -> None:
        if mac not in self.devices:
            for name, receiver in self.receivers.items():
                if receiver.check_type(data[4:]):
                    self.devices[mac] = name

    def log(self) -> None:
        while True:
            for _ in range(10):
                sleep(1)
                if self.stop_event.is_set():
                    return
            print(self.devices)

    def main(self) -> int:
        sock = hci_open_dev(0)
        enable_le_scan(sock, filter_duplicates=False)

        thread_bt = Thread(
            target=parse_le_advertising_events,
            kwargs={
                "sock": sock,
                "handler": self.le_advertise_packet_handler,
                "debug": False,
            },
        )
        thread_log = Thread(target=self.log)

        thread_bt.start()
        thread_log.start()

        try:
            thread_bt.join()
        except KeyboardInterrupt:
            self.stop_event.set()


if __name__ == "__main__":
    parser = ArgumentParser(description="Bluetooth LE Advertising Packet Handler")
    parser.add_argument(
        "-c", "--config", type=str, help="Path to the configuration file"
    )
    parser.add_argument(
        "-d", "--discover", action="store_true", help="Run in discovery mode"
    )
    args = parser.parse_args()

    if args.discover:
        discover = Discover()
        raise SystemExit(discover.main())
    else:
        main = Main(args.config)
        raise SystemExit(main.main())
