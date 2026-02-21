# sender.py
import sys
import socket
from packet import Packet, make_data, make_eot

SEQ_LOG = "seqnum.log"
ACK_LOG = "ack.log"

def chunk_text(s: str, n: int = 500):
    for i in range(0, len(s), n):
        yield s[i:i+n]

def main():
    if len(sys.argv) != 6:
        print("Usage: sender <emu_host> <emu_port> <sender_port> <timeout_ms> <input_file>")
        sys.exit(1)

    emu_host = sys.argv[1]
    emu_port = int(sys.argv[2])
    sender_port = int(sys.argv[3])
    timeout_ms = int(sys.argv[4])
    infile = sys.argv[5]

    emu_addr = (socket.gethostbyname(emu_host), emu_port)

    # read file
    with open(infile, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # prepare logs
    seq_f = open(SEQ_LOG, "w", encoding="utf-8")
    ack_f = open(ACK_LOG, "w", encoding="utf-8")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", sender_port))
    sock.settimeout(timeout_ms / 1000.0)

    seqnum = 1

    try:
        for chunk in chunk_text(content, 500):
            pkt = make_data(seqnum, chunk)

            while True:
                # send (or resend) the packet
                sock.sendto(pkt.to_bytes(), emu_addr)
                seq_f.write(f"{seqnum}\n")
                seq_f.flush()

                # wait for ACK
                try:
                    data, _ = sock.recvfrom(4096)
                    r = Packet.from_bytes(data)

                    if r.type == 0:
                        ack_f.write(f"{r.seqnum}\n")
                        ack_f.flush()

                        if r.seqnum == seqnum:
                            seqnum += 1
                            break
                        # else: ignore mismatched ACK (possible duplicate)
                    # else: ignore non-ACK here
                except socket.timeout:
                    # timeout -> resend same pkt
                    continue

        # all data ACKed -> send EOT
        eot = make_eot()
        sock.sendto(eot.to_bytes(), emu_addr)

        # wait for EOT from receiver (EOT never lost per spec, but still loop safely)
        while True:
            data, _ = sock.recvfrom(4096)
            r = Packet.from_bytes(data)
            if r.type == 2:
                break

    finally:
        try:
            seq_f.close()
            ack_f.close()
        except Exception:
            pass
        sock.close()

if __name__ == "__main__":
    main()