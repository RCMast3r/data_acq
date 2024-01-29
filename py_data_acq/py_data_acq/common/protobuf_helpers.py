from hytech_np_proto_py import hytech_pb2
import google.protobuf.message_factory


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
        try:
            setattr(pb_msg, key, cantools_dict[key])
        except TypeError as e:
            print(f"Caught TypeError: {e}")
            expected_type = type(getattr(pb_msg, key))
            
            try:
                converted_value = expected_type(cantools_dict[key])
                setattr(pb_msg, key, converted_value)
                print(f"Successfully set {key} to {converted_value}")
            except ValueError:
                print(f"Unable to convert {cantools_dict[key]} to {expected_type.__name__}")

    return pb_msg
