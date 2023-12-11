import asyncio
from py_data_acq.io_handler.udp_handle import UDP_Handle


# TODO we may want to have a config file handling to set params such as:
#      - file save interval for MCAP file
#      - foxglove server port
#      - foxglove server ip
#      - protobuf binary schema file location and file name
#      - config to inform io handler (say for different CAN baudrates)

async def main():

    # this queue could at some point be receiving from multiple inputs.
    # for example, we will have CAN as our only input as of right now but we may need to add in 
    # a sensor that inputs over UART or ethernet
    queue = asyncio.Queue()
    data_input = UDP_Handle("127.0.0.1", 12345)
    cor = data_input.listen(queue)
    data_input_task = asyncio.create_task(cor)

    # TODO the deserialization task 
    # TODO the foxglove websocket task
    # TODO the MCAP file task

if __name__ == "__main__":
    asyncio.run(main())
