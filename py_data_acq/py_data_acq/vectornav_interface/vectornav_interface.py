from vectornav_lib import *
import asyncio
import can
import concurrent.futures

# TODO import standard foxglove protos
# TODO import generated vectornav protos

async def continuous_standalone_vn_receiver(queue, q2, message_classes):
    vn = VNUSB_lib(sys.argv[1], 115200)
    while True:
        # Wait for the next message
        result = await vn.poll_data_async()
        print(results)

        # data = QueueData(msg.DESCRIPTOR.name, msg)
        # await queue.put(data)
    # await q2.put(data)
    
    # Don't forget to stop the notifier to clean up resources.
    notifier.stop()

