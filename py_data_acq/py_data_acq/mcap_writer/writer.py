import asyncio
import sys
import time
from mcap_protobuf.writer import Writer
import google.protobuf.message_factory
from collections import namedtuple

from datetime import datetime

from typing import (
    Any,
    Optional,
    Set
)

# TODO make these an environmental thing for nix
# from py_data_acq.mcap_writer import all_msgs_pb2
# from py_data_acq.mcap_writer import ht_data_pb2

# TODO move this into a schema / descriptor associator util module or class
def list_of_message_names():
    message_names = []
    # Iterate through all attributes in the generated module
    for attr_name in dir(ht_data_pb2):
        # Check if the attribute is a class and if it's a message type
        attr = getattr(ht_data_pb2, attr_name)
        if isinstance(attr, type) and hasattr(attr, 'DESCRIPTOR'):
            message_names.append(attr.DESCRIPTOR.name)
    return message_names

class HTPBMcapWriter(Writer):
    def __init__(self, mcap_base_path):
        self.base_path = mcap_base_path
        messages = list_of_message_names()
        self.message_classes = {}
        now = datetime.now()
        date_time_filename = now.strftime("%m_%d_%Y_%H_%M_%S"+".mcap")
        self.writing_file = open(date_time_filename, "wb")
        super().__init__(self.writing_file)
        # creating message classes via the classes available in ht_data
        for name in messages: 
            self.message_classes[name] = google.protobuf.message_factory.GetMessageClass(ht_data_pb2.DESCRIPTOR.message_types_by_name.get(name))
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
        print(int(time.time()))
        super().write_message(topic="/ht_data", message=msg, log_time=int(time.time_ns()), publish_time=int(time.time_ns()))
        return True
    # async def open_new(self, )

    # gets the list of names via type inflection
    # 
    async def write_data(self, queue):

        data = await queue.get()
        if data is not None:
            # des_msg = all_msgs_pb2.hytech_msg()
            # des_msg.ParseFromString(data)
            des_msg = ht_data_pb2.ht_data()
            # if des_msg in self.message_classes:
            # msg = self.message_classes[des_msg.msg_id]()
            
            des_msg.ParseFromString(data)
            print(des_msg)
            # TODO make this awaitable
            print("writing")
            return await self.write_msg(des_msg)
            # else: 
                # print(des_msg.msg_id)
                # print("asdf")
                # return True
    
                
