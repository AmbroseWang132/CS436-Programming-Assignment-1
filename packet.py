# packet.py
from dataclasses import dataclass
import struct

# Packet format:
# 3 unsigned 32-bit integers: type, seqnum, length
# followed by 'length' bytes of UTF-8 data
_HEADER_FMT = "!III"
_HEADER_SIZE = struct.calcsize(_HEADER_FMT)
MAX_DATA_LEN = 500

@dataclass
class Packet:
    type: int      # 0 ACK, 1 DATA, 2 EOT
    seqnum: int
    length: int
    data: str

    def to_bytes(self) -> bytes:
        if self.type not in (0, 1, 2):
            raise ValueError("Invalid packet type")
        if self.type == 0:
            payload = b""
            length = 0
        elif self.type == 2:
            payload = b""
            length = 0
        else:
            # DATA
            if len(self.data) > MAX_DATA_LEN:
                raise ValueError("DATA too long (>500 chars)")
            payload = self.data.encode("utf-8")
            length = len(self.data)

        header = struct.pack(_HEADER_FMT, int(self.type), int(self.seqnum), int(length))
        return header + payload

    @staticmethod
    def from_bytes(b: bytes) -> "Packet":
        if len(b) < _HEADER_SIZE:
            raise ValueError("Packet too short")
        ptype, seqnum, length = struct.unpack(_HEADER_FMT, b[:_HEADER_SIZE])
        payload = b[_HEADER_SIZE:]

        if ptype in (0, 2):
            return Packet(int(ptype), int(seqnum), 0, "")
        else:
            # DATA: read payload as utf-8 text
            data = payload.decode("utf-8", errors="replace")
            if length != len(data):
                length = len(data)
            return Packet(int(ptype), int(seqnum), int(length), data)

def make_ack(seqnum: int) -> Packet:
    return Packet(0, seqnum, 0, "")

def make_data(seqnum: int, data: str) -> Packet:
    return Packet(1, seqnum, len(data), data)

def make_eot() -> Packet:
    return Packet(2, 0, 0, "")