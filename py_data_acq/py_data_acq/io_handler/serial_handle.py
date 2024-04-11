import serial_asyncio
import cantools
from ..common import protobuf_helpers
from ..common.common_types import QueueData


async def check_sync_byte(reader):
    byte_guy = await reader.read(1)
    if byte_guy == 0xFA:
        return True
    else:
        return False


async def serial_reciever(can_db: cantools.db.Database, message_classes, q1, q2):
    # Start asyncio on the port
    reader, writer = await serial_asyncio.open_serial_connection(
        url="/dev/xboi", baudrate=115200
    )

    while True:
        try:
            # if check_sync_byte(reader):
            # Wait for the next message from the buffer, then break it into parts using the byte value for ","
            decoded_msg = None
            sync_msg = await reader.readuntil(b'\n\xff\n')
            frameid = int.from_bytes(sync_msg[0:2], byteorder="little")
            msg = can_db.get_message_by_frame_id(frameid)
            payload = sync_msg[2:-3]
            # Break down message
            decoded_msg = can_db.decode_message(
                frameid, payload, decode_containers=True, decode_choices=True
            )
            # Package as protobuf guy
            msg = protobuf_helpers.pack_protobuf_msg(
                decoded_msg, msg.name.lower(), message_classes
            )
            data = QueueData(msg.DESCRIPTOR.name, msg)
            # Throw data into queues and start again
            await q1.put(data)
            await q2.put(data)

        except (KeyError, TypeError, ValueError, IndexError) as e:
            print(f"Error decoding frame, error : {e}")
            if decoded_msg:
                print(f"error msg: {decoded_msg}")
            continue
