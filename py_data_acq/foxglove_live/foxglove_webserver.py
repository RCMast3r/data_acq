import asyncio

from foxglove_websocket import run_cancellable

from foxglove_websocket.server import FoxgloveServer

import os
import ht_data_pb2
from base64 import standard_b64encode
import socket
import time




with open(
    os.path.join(os.path.dirname(ht_data_pb2.__file__), "ht_data.bin"), "rb"
) as schema_bin:
    schema_base64 = standard_b64encode(schema_bin.read()).decode("ascii")



async def listen_for_messages():

    async with FoxgloveServer("0.0.0.0", 8765, "example server") as fs:
        chan_id = await fs.add_channel(
            {
                "topic": "yo",
                "encoding": "protobuf",
                "schemaName": "ht_data",
                "schema": schema_base64,
            }
        )
        try:
            while True:
                data, addr = await asyncio.to_thread(sock.recvfrom, 1024)
                await fs.send_message(
                    chan_id,
                    time.time_ns(),
                    data)
                # Note: 'data' contains the serialized message, but we're not decoding it here
        except asyncio.CancelledError:
            pass
        finally:
            sock.close()

async def main():
    listen_task = asyncio.create_task(listen_for_messages())

    try:
        await listen_task
    except KeyboardInterrupt:
        listen_task.cancel()
        await listen_task


if __name__ == "__main__":
    asyncio.run(main())
