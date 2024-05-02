import asyncio

import time
from mcap_protobuf.writer import Writer
from datetime import datetime
from typing import Any, Optional, Set
import os


class HTPBMcapWriter:
    def __init__(self, mcap_base_path, init_writing: bool):
        self.base_path = mcap_base_path
        if init_writing:
            now = datetime.now()
            date_time_filename = now.strftime("%m_%d_%Y_%H_%M_%S" + ".mcap")
            self.actual_path = os.path.join(mcap_base_path, date_time_filename)
            self.writing_file = open(self.actual_path, "wb")
            self.mcap_writer_class = Writer(self.writing_file)
            self.is_writing = True
        else:
            self.is_writing = False
            self.actual_path = None
            self.writing_file = None
            self.mcap_writer_class = None

    def __await__(self):
        async def closure():
            print("await")
            return self

        return closure().__await__()

    def __enter__(self):
        return self

    def __exit__(self, exc_, exc_type_, tb_):
        self.mcap_writer_class.finish()
        self.writing_file.close()

    def __aenter__(self):
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, traceback: Any):
        self.mcap_writer_class.finish()
        self.writing_file.close()

    async def close_writer(self):
        if self.is_writing:
            self.is_writing = False
            self.mcap_writer_class.finish()
            self.writing_file.close()

        return True

    async def open_new_writer(self, metadata=None):
        if self.is_writing:
            self.is_writing = False
            self.mcap_writer_class.finish()
            self.writing_file.close()

        #dt = datetime.strptime(str(metadata["time"])[:24], "%a %b %d %Y %H:%M:%S")
        #dt = dt.strftime("%Y-%m-%d-T%H-%M-%S")
        date_time_filename = str(metadata["time"])+".mcap"
        print(os.path.join(self.base_path, date_time_filename))
        print(metadata)

        self.actual_path = os.path.join(self.base_path, date_time_filename)
        self.writing_file = open(self.actual_path, "wb")
        self.mcap_writer_class = Writer(self.writing_file)

        #if metadata is not None:
        #    await self.write_metadata("setup", metadata)

        self.is_writing = True
        return True

    async def write_msg(self, msg):
        if self.is_writing:
            self.mcap_writer_class.write_message(
                topic=msg.DESCRIPTOR.name + "_data",
                message=msg,
                log_time=int(time.time_ns()),
                publish_time=int(time.time_ns()),
            )
            self.writing_file.flush()
        return True

    async def write_metadata(self, name, metadata):
        self.mcap_writer_class._writer.add_metadata(name, metadata)

    async def write_data(self, msg):
        if msg is not None:
            return await self.write_msg(msg.pb_msg)
