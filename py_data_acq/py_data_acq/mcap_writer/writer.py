import asyncio

import time
from mcap_protobuf.writer import Writer
from datetime import datetime
from typing import (
    Any,
    Optional,
    Set
)

class HTPBMcapWriter(Writer):
    def __init__(self, mcap_base_path, msg_names: list[str], msg_classes):
        self.base_path = mcap_base_path
        messages = msg_names
        self.message_classes = msg_classes
        now = datetime.now()
        date_time_filename = now.strftime("%m_%d_%Y_%H_%M_%S"+".mcap")
        self.writing_file = open(date_time_filename, "wb")
        super().__init__(self.writing_file)

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
    
    async def write_msg(self, msg):
        
        super().write_message(topic=msg.DESCRIPTOR.name+"_data", message=msg, log_time=int(time.time_ns()), publish_time=int(time.time_ns()))
        return True

    async def write_data(self, queue):
        msg = await queue.get()
        if msg is not None:
            return await self.write_msg(msg.pb_msg)
            
    
                
