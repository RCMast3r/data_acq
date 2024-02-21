import os
import can
import asyncio
import cantools
from can.interfaces.udp_multicast import UdpMulticastBus

can_methods = {
    "debug": [UdpMulticastBus.DEFAULT_GROUP_IPv6, "udp_multicast"],
    "local_can_usb_KV": [0, "kvaser"],
    "local_debug": ["vcan0", "socketcan"],
}


def find_can_interface():
    """Find a CAN interface by checking /sys/class/net/."""
    for interface in os.listdir("/sys/class/net/"):
        if interface.startswith("can"):
            return interface
    return None


def init_can():
    can_interface = find_can_interface()

    if can_interface:
        print(f"Found CAN interface: {can_interface}")
        try:
            # Attempt to initialize the CAN bus
            bus = can.interface.Bus(channel=can_interface, bustype="socketcan")
            print(f"Successfully initialized CAN bus on {can_interface}")
            # Interface exists and bus is initialized, but this doesn't ensure the interface is 'up'
        except can.CanError as e:
            print(f"Failed to initialize CAN bus on {can_interface}: {e}")
            print("defaulting to using virtual can interface vcan0")
            bus = can.Bus(
                interface="socketcan", channel="vcan0", receive_own_messages=True
            )
    else:
        print("defaulting to using virtual can interface vcan0")
        bus = can.Bus(interface="socketcan", channel="vcan0", receive_own_messages=True)

    return bus


async def can_receiver(
    can_msg_decoder: cantools.db.Database, message_classes, queue, q2
):
    # Get bus
    can_bus = init_can()

    loop = asyncio.get_event_loop()
    reader = can.AsyncBufferedReader()
    notifier = can.Notifier(can_bus, [reader], loop=loop)

    while True:
        # Wait for the next message from the buffer
        msg = await reader.get_message()
        try:
            decoded_msg = can_msg_decoder.decode_message(
                msg.arbitration_id, msg.data, decode_containers=True
            )
            msg = can_msg_decoder.get_message_by_frame_id(msg.arbitration_id)
            msg = pb_helpers.pack_protobuf_msg(
                decoded_msg, msg.name.lower(), message_classes
            )
            data = QueueData(msg.DESCRIPTOR.name, msg)
            # await asyncio.sleep(1)
            await queue.put(data)
            await q2.put(data)
        except:
            pass

    # Don't forget to stop the notifier to clean up resources.
    notifier.stop()
