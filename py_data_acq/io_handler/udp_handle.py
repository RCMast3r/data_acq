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
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        # Code executed when exiting the context
        # Clean-up operations or resource releasing would go here
        if exc_type is not None:
            # Handle exceptions if needed
            print(f"Exception occurred: {exc_type}, {exc_value}")
        # Perform any necessary clean-up
        # Close files, release resources, etc.
        print("Exiting the context")

    def __aenter__(self):
        print("asdf")
        return self
    def __aexit__(self, exc_type, exc_value, traceback):
        # Actions to be taken after exiting the 'with' block
        print("Exiting the context")
        # You can handle exceptions here if needed
        if exc_type:
            print(f"Exception occurred: {exc_type}, {exc_value}")
        # Return True to suppress exceptions or False to propagate them
        return True  # Change to False if you want to propagate exceptions

    def attempt_recv(self, queue):
        try:
            data, address = self.sock.recvfrom(1024)
            if data:
                queue.put_nowait(data)  # Put data into the queue
                print("recvd")
        except socket.error as e:
            if e.errno != socket.errno.EWOULDBLOCK:
                # Handle other socket errors if needed
                print("Socket error:", e)

