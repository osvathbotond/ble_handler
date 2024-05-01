from influxdb_client import InfluxDBClient
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from senders._abc import Sender
from receivers._abc import Receiver
from utils.plugin_manager import register_sender


@register_sender("influxdb")
class InfluxDBSender(Sender):
    def setup(self, config: dict) -> None:
        address = config["address"]
        port = config["port"]
        token = config["token"]
        org = config["org"]
        self.bucket = config["bucket"]

        if address.startswith(("http://", "https://")):
            url = f"{address}:{port}"
        else:
            url = f"http://{address}:{port}"

        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def teardown(self) -> None:
        return

    def send_message(self, name: str, settings: dict, receiver: Receiver) -> None:
        p = Point(settings["measurement"])

        for key, value in receiver.to_json(name).items():
            match settings["typemap"][key]:
                case "time":
                    p.time(value, "s")
                case "tag":
                    p.tag(key, value)
                case "field":
                    p.field(key, value)
                case other:
                    raise ValueError(
                        f'Invalid option in typemap for device {name}: "{other}"'
                    )

        self.write_api.write(bucket=self.bucket, record=p)
