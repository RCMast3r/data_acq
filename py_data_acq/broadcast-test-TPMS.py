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
 
    msg = db.get_message_by_name("MC1_TORQUE_COMMAND")
    rpm = db.get_message_by_name("MC4_SETPOINTS_COMMAND")
    tpmsLF_msg = db.get_message_by_name("LF_TTPMS_1")
    tpmsLR_msg = db.get_message_by_name("LR_TTPMS_1")
    tpmsRF_msg = db.get_message_by_name("RF_TTPMS_1")
    tpmsRR_msg = db.get_message_by_name("RR_TTPMS_1")

    data = msg.encode({'torque_command': 100})
    msg = can.Message(arbitration_id=msg.frame_id, is_extended_id=False, data=data)

    tpmsLF_data = tpmsLF_msg.encode({'LF_TTPMS_SN': 100, 'LF_TTPMS_BAT_V': 100, 'LF_TTPMS_P': 20, 'LF_TTPMS_P_GAUGE': 20})
    tpmsLF_msg = can.Message(arbitration_id=tpmsLF_msg.frame_id, is_extended_id=False, data=tpmsLF_data)

    tpmsLR_data = tpmsLR_msg.encode({'LR_TTPMS_SN': 100, 'LR_TTPMS_BAT_V': 100, 'LR_TTPMS_P': 20, 'LR_TTPMS_P_GAUGE': 20})
    tpmsLR_msg = can.Message(arbitration_id=tpmsLR_msg.frame_id, is_extended_id=False, data=tpmsLR_data)

    tpmsRF_data = tpmsRF_msg.encode({'RF_TTPMS_SN': 100, 'RF_TTPMS_BAT_V': 100, 'RF_TTPMS_P': 20, 'RF_TTPMS_P_GAUGE': 20})
    tpmsRF_msg = can.Message(arbitration_id=tpmsRF_msg.frame_id, is_extended_id=False, data=tpmsRF_data)

    tpmsRR_data = tpmsRR_msg.encode({'RR_TTPMS_SN': 100, 'RR_TTPMS_BAT_V': 100, 'RR_TTPMS_P': 20, 'RR_TTPMS_P_GAUGE': 20})
    tpmsRR_msg = can.Message(arbitration_id=tpmsRR_msg.frame_id, is_extended_id=False, data=tpmsRR_data)


    rpm_set = 100
    while(1):
        try:
            rpm_set= rpm_set+1
            bus1.send(msg)
            rpm_data = rpm.encode({'negative_torque_limit': 1, 'positive_torque_limit': 1, 'speed_setpoint_rpm': rpm_set, 'remove_error': 1, 'driver_enable': 1, 'hv_enable': 1, 'inverter_enable': 1})
            rpm_msg = can.Message(arbitration_id=rpm.frame_id, is_extended_id=False, data=rpm_data)
            bus1.send(rpm_msg)

            bus1.send(tpmsLF_msg)
            bus1.send(tpmsLR_msg)
            bus1.send(tpmsRF_msg)
            bus1.send(tpmsRR_msg)

            print("Message sent on {}".format(bus1.channel_info))
        except can.CanError:
            print("Message NOT sent!  Please verify can0 is working first")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
