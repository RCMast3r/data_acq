#!/usr/bin/env python

import asyncio

from py_data_acq.foxglove_live.foxglove_ws import HTProtobufFoxgloveServer
from py_data_acq.mcap_writer.writer import HTPBMcapWriter
from py_data_acq.mcap_writer.writer_control import WriterControlService
from py_data_acq.common.common_types import QueueData
import py_data_acq.common.protobuf_helpers as pb_helpers

import logging
from systemd.journal import JournalHandler

import os

import can
from can.interfaces.udp_multicast import UdpMulticastBus
import cantools

import grpc
from writer_control_proto_py import writer_control_pb2
from writer_control_grpc_py import writer_control_pb2_grpc


# TODO we may want to have a config file handling to set params such as:
#      - file save interval for MCAP file
#      - foxglove server port
#      - foxglove server ip
#      - protobuf binary schema file location and file name
#      - config to inform io handler (say for different CAN baudrates) and / or what sort of CAN handler to use
#      - config to say whether or not to start the service while recording or to await user to start the recording
 
async def continuous_can_receiver(can_msg_decoder: cantools.db.Database, message_classes, queue, q2):
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
            msg = await reader.get_message()
            decoded_msg = can_msg_decoder.decode_message(msg.arbitration_id, msg.data, decode_containers=True)
            msg = can_msg_decoder.get_message_by_frame_id(msg.arbitration_id)
            msg = pb_helpers.pack_protobuf_msg(decoded_msg, msg.name.lower(), message_classes)

            data = QueueData(msg.DESCRIPTOR.name, msg)
            await queue.put(data) and q2.put(data)

async def write_data_to_mcap(queue, mcap_writer):
    async with mcap_writer as mcw:
        while True:
            await mcw.handle_input_data(queue)

async def fxglv_websocket_consume_data(queue, foxglove_server):
    async with foxglove_server as fz:
        while True:
            await fz.send_msgs_from_queue(queue)

async def main():
    
    # for example, we will have CAN as our only input as of right now but we may need to add in 
    # a sensor that inputs over UART or ethernet
    server = grpc.aio.server()
    writer_control_pb2_grpc.add_WriterControlServicer_to_server(
        RecordingService(), server)
    
    queue = asyncio.Queue()
    queue2 = asyncio.Queue()


    path_to_bin = os.environ.get('BIN_PATH')
    path_to_dbc = os.environ.get('DBC_PATH')
    full_path = os.path.join(path_to_bin, "hytech.bin")
    full_path_to_dbc = os.path.join(path_to_dbc, "hytech.dbc")
    db = cantools.db.load_file(full_path_to_dbc)


    list_of_msg_names, msg_pb_classes = pb_helpers.get_msg_names_and_classes()
    fx_s = HTProtobufFoxgloveServer("0.0.0.0", 8765, "asdf", full_path, list_of_msg_names)
    
    mcap_writer = HTPBMcapWriter(".", init_on_create=True)
    
    receiver_task = asyncio.create_task(continuous_can_receiver(db, msg_pb_classes, queue, queue2))           
    fx_task = asyncio.create_task(fxglv_websocket_consume_data(queue, fx_s))
    mcap_task = asyncio.create_task(write_data_to_mcap(queue2, mcap_writer))
    
    
    await asyncio.gather(receiver_task, fx_task, mcap_task)

if __name__ == "__main__":
    asyncio.run(main())