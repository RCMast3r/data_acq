import asyncio
import os
import time
from mcap_protobuf.writer import Writer
from datetime import datetime
from typing import Any, Optional, Set


class HTPBMcapWriter(Writer):
    def __init__(self, mcap_base_path: str, init_on_create: bool):
        self.base_path = mcap_base_path
        self.stopped = asyncio.Event()
        self.file_open = asyncio.Event()
        self.pause_writing_event = asyncio.Event()
        self.pause_writing_event.set()
        if init_on_create:
            self.start_new_log()

    def start_new_log(self):
        now = datetime.now()
        # if we have a file open right now, close it and open a new one
        # TODO need to ensure that while
        if self.file_open.is_set():
            self.finish_logging_to_file()
            self.file_open.clear()

        date_time_filename = now.strftime("%m_%d_%Y_%H_%M_%S" + ".mcap")
        super().__init__(open(os.path.join(self.base_path, date_time_filename), "wb"))
        self.file_open.set()

    async def finish_logging_to_file(self):
        super().finish()
        self.file_open.clear()

    def __await__(self):
        async def closure():
            print("await")
            return self

        return closure().__await__()

    def __enter__(self):
        return self

    def __exit__(self, exc_, exc_type_, tb_):
        super().finish()

    def __aenter__(self):
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, traceback: Any):
        return super().finish()

    async def write_msg(self, msg, time_recvd):
        super().write_message(
            topic=msg.DESCRIPTOR.name + "_data",
            message=msg,
            log_time=time_recvd,
            publish_time=time_recvd,
        )
        return True

    async def handle_input_data(self, queue):
        await self.file_open.wait()
        await self.pause_writing_event.wait()
        msg = await queue.get()

        if not self.stopped.is_set() and msg is not None:
            return await self.write_msg(msg.pb_msg, msg.time_received)

        if not self.pause_writing_event.is_set():
            print("not writing msgs, paused. holding in queue")
