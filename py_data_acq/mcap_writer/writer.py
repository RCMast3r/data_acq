import asyncio
import sys
import time
from mcap_protobuf.writer import Writer
import google.protobuf.message_factory
from collections import namedtuple

from typing import (
    Any,
    Optional,
    Set
)

# TODO make these an environmental thing for nix
import all_msgs_pb2
import ht_data_pb2
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
        names = list_of_message_names()
        self.message_classes = []
        for name in names: 
            self.message_classes.append({name, google.protobuf.message_factory.GetMessageClass(ht_data_pb2.DESCRIPTOR.message_types_by_name.get(name))})
    def __enter__(self):
        return self
    def __exit__(self, exc_, exc_type_, tb_):
        super().finish()
    def __aenter__(self):

        return self
    async def __aexit__(self, exc_type: Any, exc_val: Any, traceback: Any):
        return super().finish()

    # gets the list of names via type inflection

    async def write_data(self, queue):
        try:
            data = await queue.get()
            if data is not None:
                des_msg = all_msgs_pb2.hytech_msg()
                des_msg.ParseFromString(data)
                
