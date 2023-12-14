import asyncio
from typing import Any

from foxglove_websocket import run_cancellable

from foxglove_websocket.server import FoxgloveServer


from base64 import standard_b64encode
import time


# what I want to do with this class is extend the foxglove server to make it where it creates a protobuf schema
# based foxglove server that serves data from an asyncio queue.
class HTProtobufFoxgloveServer(FoxgloveServer):
    def __init__(self, host: str, port: int, name: str, pb_bin_file_path: str):
        super().__init__(host, port, name)
        self.path = pb_bin_file_path
        
        self.schema = standard_b64encode(open(pb_bin_file_path, "rb").read()).decode("ascii")
        
    # this is run when we use this in a with statement for context management
    async def __aenter__(self): 
        await super().__aenter__()
        self.chan_id = await super().add_channel(
            {
                "topic": "car data",
                "encoding": "protobuf",
                "schemaName": "ht_data",
                "schema": self.schema,
            }
        )
        
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, traceback: Any):
        return await super().__aexit__(exc_type, exc_val, traceback)

    async def send_msgs_from_queue(self, queue):
        try:
            data = await queue.get()
            if data is not None:
                await super().send_message(self.chan_id, time.time_ns(), data)
        except asyncio.CancelledError:
            pass
