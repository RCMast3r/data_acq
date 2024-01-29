#!/usr/bin/env python
import socket
import time
import math
import can
from can.interfaces.udp_multicast import UdpMulticastBus
import cantools
from pprint import pprint
import os

from hytech_np_proto_py import hytech_pb2

# Define the IP and port for the UDP socket
# bus1 = can.interface.Bus('can0', bustype='virtual')
def generate_sine_wave(amplitude, frequency, phase_shift, time_variable):
    return amplitude * math.sin(2 * math.pi * frequency * time_variable + phase_shift)

bus1 = can.Bus(channel=UdpMulticastBus.DEFAULT_GROUP_IPv6, interface='udp_multicast')
def main():
    path_to_dbc = os.environ.get('DBC_PATH')
    full_path = os.path.join(path_to_dbc, "hytech.dbc") 
    # Serialize the message to bytes
    db = cantools.database.load_file(full_path)
 
    # msg = db.get_message_by_name("M166_Current_Info")
    rpm = db.get_message_by_name("M165_Motor_Position_Info")
    value=100
    # data = msg.encode({"D4_DC_Bus_Current": 100,"D1_Phase_A_Current":int(value),"D2_Phase_B_Current":int(value),"D3_Phase_C_Current":int(value)})
    
    # msg = can.Message(arbitration_id=msg.frame_id, is_extended_id=False, data=data)
    # print(msg)
    rpm_set = 100
    while(1):
        try:
            # rpm_set= rpm_set+1
            # bus1.send(msg)
            rpm_set = generate_sine_wave(3000,1,90,time.time()) + 3000
            rpm_data = rpm.encode({'D4_Delta_Resolver_Filtered': int(1), 'D3_Electrical_Output_Frequency': int(1), 'D2_Motor_Speed': rpm_set, 'D1_Motor_Angle_Electrical': int(1)})
            rpm_msg = can.Message(arbitration_id=rpm.frame_id, is_extended_id=False, data=rpm_data)
            bus1.send(rpm_msg)

            print("Message sent on {}".format(bus1.channel_info))
        except can.CanError:
            print("Message NOT sent!  Please verify can0 is working first")
        time.sleep(0.01)

if __name__ == "__main__":
    main()
