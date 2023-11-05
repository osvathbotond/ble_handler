from receivers._abc import Receiver
from utils.plugin_manager import register_receiver

try:
    from receivers._pvvx_data import PVVXData as PVVXData


    register_receiver("pvvx")(PVVXData)

except ImportError as e:
    from dataclasses import dataclass
    from datetime import datetime

    from utils.bluetooth_utils import raw_packet_to_str


    @register_receiver("pvvx")
    @dataclass
    class PVVXData(Receiver):
        size: int
        uid: int
        UUID: int
        MAC: list[int]
        temperature: int
        humidity: int
        battery_mv: int
        battery_level: int
        counter: int
        flags: int
        timestamp: int

        def to_json(self, name: str) -> dict:
            return {
                    "name": name,
                    "timestamp": self.timestamp,
                    "temperature": self.temperature/100,
                    "humidity": self.humidity/100,
                    "battery": self.battery_level,
                    }

        @staticmethod
        def check_type(message: bytes) -> bool:
            message_str = raw_packet_to_str(message)
            message_bytearray = bytearray.fromhex(message_str)
            try:
                return message_bytearray[0] == 18 and int.from_bytes(message_bytearray[2:4], byteorder='little', signed=False) == 6170
            except IndexError:
                return False

        @classmethod
        def from_message(cls, message: bytes):
            message_str = raw_packet_to_str(message)
            message_bytearray = bytearray.fromhex(message_str)
        
            return cls(
                       size=message_bytearray[0],
                       uid=message_bytearray[1],
                       UUID=int.from_bytes(message_bytearray[2:4], byteorder='little', signed=False),
                       MAC=[message_bytearray[4+i] for i in range(6)],
                       temperature=int.from_bytes(message_bytearray[10:12], byteorder='little', signed=True),
                       humidity=int.from_bytes(message_bytearray[12:14], byteorder='little', signed=False),
                       battery_mv=int.from_bytes(message_bytearray[14:16], byteorder='little', signed=False),
                       battery_level=message_bytearray[16],
                       counter=message_bytearray[17],
                       flags=message_bytearray[18],
                       timestamp=int(datetime.now().timestamp()),
                       )
