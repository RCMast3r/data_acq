import serial_asyncio
import cantools
from ..common import protobuf_helpers
from ..common.common_types import QueueData


def check_sync_byte(reader):
    byte_guy = reader.read(1)
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
            if check_sync_byte(reader):
                # Wait for the next message from the buffer, then break it into parts using the byte value for ","
                sync_msg = await reader.readexactly(12)
                frameid = int.from_bytes(sync_msg[0:4], byteorder="little")
                msg = can_db.get_message_by_frame_id(frameid)

                # Break down message
                decoded_msg = can_db.decode_message(
                    frameid, sync_msg[4:12], decode_containers=True
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
        except (KeyError, TypeError, ValueError, IndexError) as e:
            print(f"Error decoding frame, error : {e}")
            continue
