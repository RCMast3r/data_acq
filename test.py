import asyncio
from py_data_acq.io_handler.udp_handle import UDP_Handle
from py_data_acq.foxglove_live.foxglove_ws import HTProtobufFoxgloveServer
import logging 
from systemd.journal import JournalHandler
import concurrent.futures
import threading

import asyncudp

# log = logging.getLogger('data_writer_service')
# log.addHandler(JournalHandler())
# log.setLevel(logging.INFO)

# TODO we may want to have a config file handling to set params such as:
#      - file save interval for MCAP file
#      - foxglove server port
#      - foxglove server ip
#      - protobuf binary schema file location and file name
#      - config to inform io handler (say for different CAN baudrates)

async def continuous_udp_receiver(queue, q2):
    sock = await asyncudp.create_socket(local_addr=('127.0.0.1', 12345))
    while True:

        data, addr = await sock.recvfrom()
        await queue.put(data)
        await q2.put(data)
    
async def consume_data(queue, foxglove_server):
    async with foxglove_server as fz:
        while True:
            await fz.send_msgs_from_queue(queue)

async def main():
    
    # for example, we will have CAN as our only input as of right now but we may need to add in 
    # a sensor that inputs over UART or ethernet
    queue = asyncio.Queue()
    queue2 = asyncio.Queue()
    
    fx_s = HTProtobufFoxgloveServer("0.0.0.0", 8765, "asdf", "/home/ben/hytech/data_acq/py_data_acq/foxglove_live/ht_data.bin")
    receiver_task = asyncio.create_task(continuous_udp_receiver(queue, queue2))
    
    # TODO the deserialization task for unpacking received data. 
    fx_task = asyncio.create_task(consume_data(queue, fx_s))
     
    # TODO the data consuming MCAP file task for writing MCAP files to specific directory
    
    await asyncio.gather(receiver_task, fx_task)

if __name__ == "__main__":
    asyncio.run(main())
