# nEmulator.py
import sys
import socket
import random
from packet import Packet

def vprint(verbose: bool, msg: str):
    if verbose:
        print(msg, flush=True)

def main():
    if len(sys.argv) != 8:
        print("Usage: nEmulator <emu_port> <recv_addr> <recv_port> <send_addr> <send_port> <prob> <verbose(0/1)>")
        sys.exit(1)

    emu_port = int(sys.argv[1])
    recv_addr = socket.gethostbyname(sys.argv[2])
    recv_port = int(sys.argv[3])
    send_addr = socket.gethostbyname(sys.argv[4])
    send_port = int(sys.argv[5])
    prob = float(sys.argv[6])
    verbose = (int(sys.argv[7]) == 1)

    receiver = (recv_addr, recv_port)
    sender = (send_addr, send_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", emu_port))

    vprint(verbose, f"nEmulator listening on UDP {emu_port}")
    vprint(verbose, f"Forward DATA/EOT sender({sender}) -> receiver({receiver}), drop prob={prob}")
    vprint(verbose, f"Forward ACK/EOT receiver({receiver}) -> sender({sender}), no drop")

    while True:
        data, addr = sock.recvfrom(8192)
        try:
            pkt = Packet.from_bytes(data)
        except Exception:
            # If malformed, drop
            vprint(verbose, f"Malformed packet from {addr}, dropped")
            continue

        # Determine direction:
        from_sender = (addr[0] == sender[0] and addr[1] == sender[1])

        if from_sender:
            # sender -> receiver
            if pkt.type == 1:
                vprint(verbose, f"recv DATA seq={pkt.seqnum} from sender")
                if random.random() < prob:
                    vprint(verbose, f"discard DATA seq={pkt.seqnum}")
                else:
                    sock.sendto(data, receiver)
                    vprint(verbose, f"forward DATA seq={pkt.seqnum}")
            elif pkt.type == 2:
                vprint(verbose, "recv EOT from sender; forward EOT")
                sock.sendto(data, receiver)
            else:
                vprint(verbose, f"recv type={pkt.type} from sender; forward")
                sock.sendto(data, receiver)
        else:
            # receiver -> sender
            if pkt.type == 0:
                vprint(verbose, f"recv ACK seq={pkt.seqnum} from receiver; forward ACK")
            elif pkt.type == 2:
                vprint(verbose, "recv EOT from receiver; forward EOT")
            else:
                vprint(verbose, f"recv type={pkt.type} from receiver; forward")

            sock.sendto(data, sender)

if __name__ == "__main__":
    main()