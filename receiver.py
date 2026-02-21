# receiver.py
import sys
import socket
from packet import Packet, make_ack, make_eot

ARRIVAL_LOG = "arrival.log"

def main():
    if len(sys.argv) != 5:
        print("Usage: receiver <emu_host> <emu_port> <receiver_port> <output_file>")
        sys.exit(1)

    emu_host = sys.argv[1]
    emu_port = int(sys.argv[2])
    receiver_port = int(sys.argv[3])
    outfile = sys.argv[4]

    emu_addr = (socket.gethostbyname(emu_host), emu_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", receiver_port))

    arrival_f = open(ARRIVAL_LOG, "w", encoding="utf-8")
    out_f = open(outfile, "w", encoding="utf-8", errors="replace")

    try:
        while True:
            data, _ = sock.recvfrom(8192)
            pkt = Packet.from_bytes(data)

            if pkt.type == 1:
                # DATA
                arrival_f.write(f"{pkt.seqnum}\n")
                arrival_f.flush()

                out_f.write(pkt.data)
                out_f.flush()

                ack = make_ack(pkt.seqnum)
                sock.sendto(ack.to_bytes(), emu_addr)

            elif pkt.type == 2:
                # EOT
                eot = make_eot()
                sock.sendto(eot.to_bytes(), emu_addr)
                break

    finally:
        try:
            arrival_f.close()
            out_f.close()
        except Exception:
            pass
        sock.close()

if __name__ == "__main__":
    main()