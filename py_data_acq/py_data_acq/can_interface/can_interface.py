import asyncio
import can
import concurrent.futures
import cantools

async def continuous_can_receiver(can_msg_decoder: cantools.db.Database, message_classes, queue, q2, can_bus):
    loop = asyncio.get_event_loop()
    reader = can.AsyncBufferedReader()
    notifier = can.Notifier(can_bus, [reader], loop=loop)

    while True:
        # Wait for the next message from the buffer
        msg = await reader.get_message()

        # print("got msg")
        id = msg.arbitration_id 
        try:
            decoded_msg = can_msg_decoder.decode_message(msg.arbitration_id, msg.data, decode_containers=True)
            msg = can_msg_decoder.get_message_by_frame_id(msg.arbitration_id)
            msg = pb_helpers.pack_protobuf_msg(decoded_msg, msg.name.lower(), message_classes)
            data = QueueData(msg.DESCRIPTOR.name, msg)
            await queue.put(data)
            await q2.put(data)
        except Exception as e:
            pass

    # Don't forget to stop the notifier to clean up resources.
    notifier.stop()

