import asyncio
import socket
import asyncudp

from py_data_acq.common.common_types import QueueData
from vn_protos_np_proto_py.vectornav_proto import wrapper_pb2
async def receive_message_over_udp(addr, port, mcap_data_out_queue, fxglv_data_out_queue, can_out_q):
    sock = await asyncudp.create_socket(local_addr=(addr, port))
    while True:
        data, addr = await sock.recvfrom()
        wrapper = wrapper_pb2.VNWrapper()
        wrapper.ParseFromString(data)
        print(wrapper)
        data_arr = []
        
        data_arr.append(QueueData(wrapper.vn_vel_data.DESCRIPTOR.name, wrapper.vn_vel_data))
        data_arr.append(QueueData(wrapper.vn_linear_accel_data.DESCRIPTOR.name, wrapper.vn_linear_accel_data))
        data_arr.append(QueueData(wrapper.vn_linear_accel_uncomp_data.DESCRIPTOR.name, wrapper.vn_linear_accel_uncomp_data))
        data_arr.append(QueueData(wrapper.vn_angular_rate_data.DESCRIPTOR.name, wrapper.vn_angular_rate_data))
        data_arr.append(QueueData(wrapper.vn_ypr_data.DESCRIPTOR.name, wrapper.vn_ypr_data))
        data_arr.append(QueueData(wrapper.vn_lat_lon_data.DESCRIPTOR.name, wrapper.vn_lat_lon_data))
        data_arr.append(QueueData(wrapper.vn_gps_time_data.DESCRIPTOR.name, wrapper.vn_gps_time_data))
        data_arr.append(QueueData(wrapper.vn_status_data.DESCRIPTOR.name, wrapper.vn_status_data))

        for data in data_arr:
            await mcap_data_out_queue.put(data)
            await fxglv_data_out_queue.put(data)
            await fxglv_data_out_queue.put(data)

