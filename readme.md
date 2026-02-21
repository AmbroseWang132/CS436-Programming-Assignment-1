# CS 436 – Program Assignment 1  
Stop-and-Wait Reliable Data Transfer Protocol  
Author: Ambrose Wang  
Quest ID: l667wang
Student ID: 20894753

---

## 1. Environment

This program was developed and tested on:

- University of Waterloo Undergraduate Linux Environment
- Ubuntu 2404-004
- Ubuntu 2404-002
- Ubuntu 2404-006

All programs were executed on the following machines:

- Host1 (Sender): 129.97.167.171
- Host2 (Receiver): 129.97.167.158
- Host3 (nEmulator): 129.97.167.172

---

## 2. Files Included

The submission contains the following files:

- sender.py — Stop-and-Wait sender implementation

- receiver.py — Stop-and-Wait receiver implementation

- nEmulator.py — Network emulator that simulates packet loss

- packet.py — Packet structure and serialization logic

- README.md — This documentation file

- input.txt — Sample input file for testing

No Makefile is required since the implementation is in Python.
---

## 3. How to Run

⚠️ IMPORTANT: Programs must be started in the following order.

nEmulator

Receiver

Sender

All parameters must be provided via command line

---

### Step 1: Start nEmulator (on Host3)

python3 nEmulator.py <emulator_port> <receiver_IP> <receiver_port> <sender_IP> <sender_port> <drop_probability> <verbose>


Example:

python3 nEmulator.py 9991 129.97.167.158 9994 129.97.167.171 9992 0.3 1


---

### Step 2: Start Receiver (on Host2)

python3 receiver.py <emulator_IP> <emulator_port> <receiver_port> <output_file>


Example:

python3 receiver.py 129.97.167.172 9991 9994 output.txt


---

### Step 3: Start Sender (on Host1)

python3 sender.py <emulator_IP> <emulator_port> <sender_port> <timeout_ms> <input_file>


Example:

python3 sender.py 129.97.167.172 9991 9992 1000 input.txt



---

## 4. Program Parameters

### sender.py
1. Emulator host address  
2. Emulator UDP port  
3. Sender UDP port  
4. Timeout interval (milliseconds)  
5. Input file name  

### receiver.py
1. Emulator host address  
2. Emulator UDP port  
3. Receiver UDP port  
4. Output file name  

### nEmulator.py
1. Emulator UDP port  
2. Receiver IP address  
3. Receiver UDP port  
4. Sender IP address  
5. Sender UDP port  
6. Packet loss probability  
7. Verbose mode (1 = on, 0 = off)

---

## 5. Output Files Generated

### Sender:
- seqnum.log
- ack.log

### Receiver:
- arrival.log
- output file

All log files follow the required format:
One sequence number per line.

---

## 6. Notes

- Sequence numbers start from 1.
- EOT packets are never dropped.
- ACK packets are never dropped.
- Packet loss applies only to DATA packets.
- Stop-and-Wait protocol is implemented using socket timeout mechanism.