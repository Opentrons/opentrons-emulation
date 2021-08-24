import can
import time


bus = "socketcan"
channel = "vcan0"


b = can.interface.Bus(channel=channel, bustype=bus)

for i in range(5):
    msg = can.Message(arbitration_id=3 << 15, data=[1, 2, 3, 4])
    b.send(msg)
    print(b.recv(1))
    time.sleep(1)
