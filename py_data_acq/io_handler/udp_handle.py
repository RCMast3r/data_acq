# this thingy will handle the receiving of the CAN data over hardware and 
# provide it to whatever needs it.

import asyncio
import socket

# I think what I want is that this thing is given some asyncio object that will serve as the data pipeline into the 2 services in the data writer service.
# this way, the hardware that is actually receiving the data can easily be switched out and between.
class UDP_Handle:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
    async def listen(self, queue):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print("got data")
            queue.put_nowait(data)
