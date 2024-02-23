#!/usr/bin/env python
import asyncio

from py_data_acq.foxglove_live.foxglove_ws import HTProtobufFoxgloveServer
from py_data_acq.mcap_writer.writer import HTPBMcapWriter
import py_data_acq.common.protobuf_helpers as pb_helpers
from py_data_acq.web_server.mcap_server import MCAPServer
from py_data_acq.io_handler.can_handle import can_receiver
from py_data_acq.io_handler.serial_handle import serial_reciever

# from py_data_acq.io_handler.serial_handle import
import sys
import os
import cantools
import logging

# TODO we may want to have a config file handling to set params such as:
#      - file save interval for MCAP file
#      - foxglove server port
#      - foxglove server ip
#      - protobuf binary schema file location and file name
#      - config to inform io handler (say for different CAN baudrates)


async def write_data_to_mcap(queue, mcap_writer):
    async with mcap_writer as mcw:
        while True:
            await mcw.write_data(queue)


async def fxglv_websocket_consume_data(queue, foxglove_server):
    async with foxglove_server as fz:
        while True:
            await fz.send_msgs_from_queue(queue)


async def run(logger):
    # Init some bois
    queue1 = asyncio.Queue()
    queue2 = asyncio.Queue()
    path_to_bin = ""
    path_to_dbc = ""

    # Get paths
    if len(sys.argv) > 2:
        path_to_bin = sys.argv[1]
        path_to_dbc = sys.argv[2]
    else:
        path_to_bin = os.environ.get("BIN_PATH")
        path_to_dbc = os.environ.get("DBC_PATH")

    # Load everything
    fp_proto = os.path.join(path_to_bin, "hytech.bin")
    fp_dbc = os.path.join(path_to_dbc, "hytech.dbc")
    db = cantools.db.load_file(fp_dbc)

    # Start foxglove websocket and send message list
    list_of_msg_names, msg_pb_classes = pb_helpers.get_msg_names_and_classes()
    fx_s = HTProtobufFoxgloveServer(
        "0.0.0.0", 8765, "asdf", fp_proto, list_of_msg_names
    )

    # Set output path of mcap files, and if on nixos save to a predefined path
    path_to_mcap = "."
    if os.path.exists("/etc/nixos"):
        logger.info("detected running on nixos")
        path_to_mcap = "/home/nixos/recordings"
    mcap_writer = HTPBMcapWriter(path_to_mcap, list_of_msg_names, True)
    mcap_server = MCAPServer(mcap_writer=mcap_writer, path=path_to_mcap)

    # Setup receiver_task to listen to CAN
    # receiver_task = asyncio.create_task(
    #     can_receiver(db, msg_pb_classes, queue1, queue2)
    # )

    # BUG: This shit breaks and crashes everything, fix it
    # And another for serial
    receiver_task = asyncio.create_task(
        serial_reciever(db, msg_pb_classes, queue1, queue2)
    )

    # Setup other guys to respective asyncio tasks
    fx_task = asyncio.create_task(fxglv_websocket_consume_data(queue1, fx_s))
    mcap_task = asyncio.create_task(write_data_to_mcap(queue2, mcap_writer))
    srv_task = asyncio.create_task(mcap_server.start_server())
    logger.info("created tasks")

    await asyncio.gather(receiver_task, fx_task, mcap_task, srv_task)


if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger("data_writer_service")
    logger.setLevel(logging.INFO)
    asyncio.run(run(logger))
