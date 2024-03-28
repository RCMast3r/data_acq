import asyncio
import socket
from vn_protos_np_proto_py.vectornav_proto import wrapper_pb2
from hytech_np_proto_py import hytech_pb2


async def send_message_over_udp(serialized_message, host="127.0.0.1", port=6000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    loop = asyncio.get_running_loop()
    sock.setblocking(False)
    await loop.sock_sendto(sock, serialized_message, (host, port))
    sock.close()


async def main():
    vn_msg = hytech_pb2.vn_ypr(vn_yaw=124.4, vn_pitch=12.0, vn_roll=12.0)

    wrapper = wrapper_pb2.VNWrapper()
    wrapper.vn_ypr_data.CopyFrom(vn_msg)  # For MessageA

    serialized_message = wrapper.SerializeToString()
    # Or, to send MessageB, comment the above and use:
    # wrapper.message_b.CopyFrom(message_b)

    await send_message_over_udp(serialized_message)


if __name__ == "__main__":
    asyncio.run(main())
