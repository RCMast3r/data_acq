#!/usr/bin/env python
import socket
import time
import can
from can.interfaces.udp_multicast import UdpMulticastBus
import cantools
from pprint import pprint
import os

from hytech_np_proto_py import hytech_pb2

# Define the IP and port for the UDP socket
# bus1 = can.interface.Bus('can0', bustype='virtual')
bus1 = can.Bus(channel=UdpMulticastBus.DEFAULT_GROUP_IPv6, interface='udp_multicast')
def main():
    path_to_dbc = os.environ.get('DBC_PATH')
    full_path = os.path.join(path_to_dbc, "hytech.dbc") 
    # Serialize the message to bytes
    db = cantools.database.load_file(full_path)
    msg = db.get_message_by_name("ID_MC1_TORQUE_COMMAND")
    print(msg.signals)
    data = msg.encode({'torque_command': 100})

    msg = can.Message(arbitration_id=msg.frame_id, is_extended_id=False, data=data)
    print(msg)
    while(1):

        try:
            bus1.send(msg)
            print("Message sent on {}".format(bus1.channel_info))
        except can.CanError:
            print("Message NOT sent!  Please verify can0 is working first")
        time.sleep(0.2)

if __name__ == "__main__":
    main()
