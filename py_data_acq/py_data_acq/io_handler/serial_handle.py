import serial_asyncio
import cantools
from ..common import protobuf_helpers
from ..common.common_types import QueueData


async def serial_reciever(can_db: cantools.db.Database, message_classes, q1, q2):
    # Start asyncio on the port
    reader, writer = await serial_asyncio.open_serial_connection(
        url="/dev/xboi", baudrate=115200
    )

    while True:
        # Wait for the next message from the buffer, then break it into parts using the byte value for ","
        nl_byte = await reader.readline()
        vals = nl_byte.split(b",")
        print(f"Raw Line: {nl_byte}")
        print(f"Comma delimited: {vals}")
        # try:
        # Get message data for foxglove
        frameid = int.from_bytes(vals[0],byteorder='little')
        try:
            msg = can_db.get_message_by_frame_id(frameid)
            # Break down message
            decoded_msg = can_db.decode_message(
                frameid, vals[1], decode_containers=True
            )

            # Package as protobuf guy
            msg = protobuf_helpers.pack_protobuf_msg(
                decoded_msg, msg.name.lower(), message_classes
            )
            data = QueueData(msg.DESCRIPTOR.name, msg)
        # Throw data into queues and start again
            await q1.put(data)
            await q2.put(data)
            # except:
            #     print("Fail")
            #     pass
        except (KeyError,TypeError,ValueError) as e:
            print(f"Error with id {frameid}, error : {e}")
            continue


