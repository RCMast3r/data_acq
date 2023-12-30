#!/usr/bin/env python

import asyncio

from py_data_acq.foxglove_live.foxglove_ws import HTProtobufFoxgloveServer
from py_data_acq.mcap_writer.writer import HTPBMcapWriter
import logging 
from systemd.journal import JournalHandler
import concurrent.futures
import threading
import os
import asyncudp
import can
from can.interfaces.udp_multicast import UdpMulticastBus
import cantools

# TODO we may want to have a config file handling to set params such as:
#      - file save interval for MCAP file
#      - foxglove server port
#      - foxglove server ip
#      - protobuf binary schema file location and file name
#      - config to inform io handler (say for different CAN baudrates)

async def continuous_can_receiver(queue, q2):
    with can.Bus(
        channel=UdpMulticastBus.DEFAULT_GROUP_IPv6, interface='udp_multicast'
    ) as bus:
        reader = can.AsyncBufferedReader()
        listeners: List[MessageRecipient] = [
            reader  # AsyncBufferedReader() listener
        ]
        loop = asyncio.get_running_loop()
        notifier = can.Notifier(bus, listeners, loop=loop)
        while True:
            # data, addr = await sock.recvfrom()
            msg = await reader.get_message()
            print(msg)
            # await queue.put(data)
            # await q2.put(data)

async def write_data_to_mcap(queue, mcap_writer):
    async with mcap_writer as mcw:
        while True:
            await mcw.write_data(queue)

async def fxglv_websocket_consume_data(queue, foxglove_server):
    async with foxglove_server as fz:
        while True:
            await fz.send_msgs_from_queue(queue)

async def main():
    
    # for example, we will have CAN as our only input as of right now but we may need to add in 
    # a sensor that inputs over UART or ethernet
    queue = asyncio.Queue()
    queue2 = asyncio.Queue()
    path_to_bin = os.environ.get('BIN_PATH')
    full_path = os.path.join(path_to_bin, "hytech.bin")
    print(full_path)
    # fx_s = HTProtobufFoxgloveServer("0.0.0.0", 8765, "asdf", full_path)

    mcap_writer = HTPBMcapWriter(".")
    
    receiver_task = asyncio.create_task(continuous_can_receiver(queue, queue2))
               
    # fx_task = asyncio.create_task(fxglv_websocket_consume_data(queue, fx_s))
    
    # in the mcap task I actually have to deserialize the any protobuf msg into the message ID and
    # the encoded message for the message id. I will need to handle the same association of message id
    # and schema in the foxglove websocket server. 
    # mcap_task = asyncio.create_task(write_data_to_mcap(queue, mcap_writer)) 
    
    # TODO the data consuming MCAP file task for writing MCAP files to specific directory
    await asyncio.gather(receiver_task)
    # await asyncio.gather(receiver_task, fx_task, mcap_task)
    # await asyncio.gather(receiver_task, mcap_task)
if __name__ == "__main__":
    asyncio.run(main())