import asyncio
import can
import concurrent.futures
import cantools
import py_data_acq.common.protobuf_helpers as pb_helpers
from py_data_acq.common.common_types import QueueData
async def continuous_can_receiver(can_msg_decoder: cantools.db.Database, message_classes, queue, q2, can_bus):
    loop = asyncio.get_event_loop()
    reader = can.AsyncBufferedReader()
    notifier = can.Notifier(can_bus, [reader], loop=loop)

    while True:
        # Wait for the next message from the buffer
        msg = await reader.get_message()
        
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

# the message queue here is filled with protobuf messages
async def continuous_can_transmitter(can_db: cantools.db.Database, can_bus, message_queue_of_msgs_to_send):
    while true:
        msg_to_send = await message_queue_of_msgs_to_send.get()
        msg, data = pb_helpers.pack_cantools_msg(msg_to_send, msg_to_send.DESCRIPTOR.name, can_db)
        msg_out = can.Message(arbitration_id=msg.frame_id, is_extended_id=False, data=data)
        await can_bus.send(msg_out)
        

    