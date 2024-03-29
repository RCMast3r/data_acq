from hytech_np_proto_py import hytech_pb2
import google.protobuf.message_factory
from cantools.database import *


def get_msg_names_and_classes():
    message_names = []
    message_classes = {}
    # Iterate through all attributes in the generated module
    for attr_name in dir(hytech_pb2):
        # Check if the attribute is a class and if it's a message type
        attr = getattr(hytech_pb2, attr_name)
        if isinstance(attr, type) and hasattr(attr, "DESCRIPTOR"):
            message_names.append(attr.DESCRIPTOR.name)
            message_classes[
                attr.DESCRIPTOR.name
            ] = google.protobuf.message_factory.GetMessageClass(
                hytech_pb2.DESCRIPTOR.message_types_by_name.get(attr.DESCRIPTOR.name)
            )
    return message_names, message_classes


def pack_protobuf_msg(cantools_dict: dict, msg_name: str, message_classes):
    if msg_name in message_classes:
        pb_msg = message_classes[msg_name]()
    for key in cantools_dict.keys():
        if(type(cantools_dict[key]) is namedsignalvalue.NamedSignalValue):
            print(msg_name)
            setattr(pb_msg, key, str(cantools_dict[key].value))
        else:
            setattr(pb_msg, key, cantools_dict[key])
    return pb_msg
