
import py_data_acq.common.protobuf_helpers as pb_helpers
from hytech_np_proto_py import hytech_pb2
from vn_protos_np_proto_py.vectornav_proto import wrapper_pb2
from can.interfaces.udp_multicast import UdpMulticastBus

import os
import cantools
import can

def main():
    path_to_dbc = os.environ.get("DBC_PATH")
    full_path_to_dbc = os.path.join(path_to_dbc, "hytech.dbc")
    db = cantools.db.load_file(full_path_to_dbc)


    bus1 = can.interface.Bus(channel=UdpMulticastBus.DEFAULT_GROUP_IPv6, interface="udp_multicast")


    msgs = []

    msgs.append(hytech_pb2.vn_ypr(vn_yaw=69.0, vn_pitch=69.0,vn_roll=69.0))
    msgs.append(hytech_pb2.vn_linear_accel(vn_lin_ins_accel_x=12, vn_lin_ins_accel_y=3, vn_lin_ins_accel_z=2))
    msgs.append(hytech_pb2.vn_linear_accel_uncomp(vn_lin_uncomp_accel_x=12, vn_lin_uncomp_accel_y=3, vn_lin_uncomp_accel_z=2))
    msgs.append(hytech_pb2.vn_vel(vn_body_vel_x=12,vn_body_vel_y= 3, vn_body_vel_z=2))
    msgs.append(hytech_pb2.vn_lat_lon(vn_gps_lat=38, vn_gps_lon=100))
    msgs.append(hytech_pb2.vn_gps_time(vn_gps_time=183098230948))
    msgs.append(hytech_pb2.vn_status(vn_gps_status="FIX_3D"))

    for pb_msg in msgs:
        msg, data = pb_helpers.pack_cantools_msg(pb_msg, pb_msg.DESCRIPTOR.name, db)
        msg_out = can.Message(arbitration_id=msg.frame_id, is_extended_id=False, data=data)
        bus1.send(msg_out)
        print(msg_out)
if __name__ == "__main__":
    main()